"""
CareerPath AI - Authentication & JWT Service
Build For Bharat 2.0 | Intelligent Talent & Workforce Ecosystem

Features:
- Cryptographic PBKDF2-SHA256 password hashing (100,000 rounds with random salt)
- Stateless JWT issuance & signature verification using PyJWT
- Supabase persistence with dual-mode storage (dedicated columns or JSONB metadata)
- Multi-role support: "candidate" (students/jobseekers) and "institution_admin" (universities)
"""

import os
import sys
import uuid
import secrets
import hashlib
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
import jwt
import logging

from backend.config import settings
from backend.database import get_supabase
from backend.models.schemas import UserRegisterRequest, UserLoginRequest, UserUpdateRequest, AuthResponse, UserResponse

logger = logging.getLogger("AuthService")

# JWT Configuration
JWT_SECRET = getattr(settings, "JWT_SECRET", "careerpath_ai_bharat_2026_super_secret_jwt_key_98234")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 72

# ==============================================================================
# 1. CRYPTOGRAPHIC PASSWORD HASHING (PBKDF2-SHA256)
# ==============================================================================
def hash_password(password: str) -> str:
    """Hashes a password with a unique salt using 100,000 iterations of PBKDF2-HMAC-SHA256."""
    salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    ).hex()
    return f"{salt}${key}"

def verify_password(plain_password: str, hashed_str: str) -> bool:
    """Verifies a plain password against the stored salt$hash string."""
    try:
        if not hashed_str or "$" not in hashed_str:
            return False
        salt, expected_key = hashed_str.split("$", 1)
        actual_key = hashlib.pbkdf2_hmac(
            'sha256',
            plain_password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        ).hex()
        return secrets.compare_digest(actual_key, expected_key)
    except Exception as e:
        logger.warning(f"Password verification error: {e}")
        return False

# ==============================================================================
# 2. JWT TOKEN GENERATION & DECODING
# ==============================================================================
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Encodes a signed JWT access token."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(hours=JWT_EXPIRATION_HOURS))
    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_access_token(token: str) -> Optional[dict]:
    """Decodes and validates a JWT token signature and expiration."""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
        logger.warning(f"Invalid JWT token: {e}")
        return None

# ==============================================================================
# 3. USER MANAGEMENT & SUPABASE PERSISTENCE
# ==============================================================================
# Local memory cache for dynamic registered accounts
_LOCAL_USERS_DB: Dict[str, dict] = {}

def register_user(req: UserRegisterRequest) -> AuthResponse:
    email_clean = req.email.strip().lower()
    supabase = get_supabase()

    # 1. Check if email already exists
    if email_clean in _LOCAL_USERS_DB:
        raise ValueError("An account with this email address already exists.")

    if supabase:
        try:
            existing = supabase.table("user_profiles").select("id").eq("email", email_clean).execute()
            if existing.data:
                raise ValueError("An account with this email address already exists.")
        except Exception as e:
            if "already exists" in str(e):
                raise e

    # 2. Hash password
    pwd_hash = hash_password(req.password)
    user_id = str(uuid.uuid4())

    user_record = {
        "id": user_id,
        "email": email_clean,
        "user_name": req.user_name.strip(),
        "password_hash": pwd_hash,
        "role": req.role,
        "institution_name": req.institution_name,
        "department": req.department,
        "graduation_year": req.graduation_year,
        "skills": req.skills or [],
        "education": [{"degree": "B.Tech", "department": req.department, "year": req.graduation_year}],
        "experience": {
            "auth": {
                "password_hash": pwd_hash,
                "role": req.role,
                "institution_name": req.institution_name,
                "department": req.department,
                "graduation_year": req.graduation_year
            }
        }
    }

    # Store locally
    _LOCAL_USERS_DB[email_clean] = user_record

    # Store in Supabase
    if supabase:
        try:
            # First try inserting with dedicated columns
            payload = {
                "id": user_id,
                "user_name": req.user_name.strip(),
                "email": email_clean,
                "skills": req.skills or [],
                "education": user_record["education"],
                "experience": user_record["experience"]
            }
            supabase.table("user_profiles").insert(payload).execute()
        except Exception as e:
            logger.warning(f"Could not persist user to Supabase: {e}")

    token = create_access_token({
        "sub": user_id,
        "email": email_clean,
        "role": req.role,
        "name": req.user_name
    })

    return AuthResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse(
            id=user_id,
            email=email_clean,
            user_name=req.user_name.strip(),
            role=req.role,
            institution_name=req.institution_name,
            department=req.department,
            graduation_year=req.graduation_year,
            skills=req.skills or []
        )
    )

def login_user(req: UserLoginRequest) -> AuthResponse:
    email_clean = req.email.strip().lower()
    supabase = get_supabase()
    user_record = None

    # Check local DB
    if email_clean in _LOCAL_USERS_DB:
        user_record = _LOCAL_USERS_DB[email_clean]
    elif supabase:
        try:
            resp = supabase.table("user_profiles").select("*").eq("email", email_clean).execute()
            if resp.data:
                row = resp.data[0]
                exp = row.get("experience") or {}
                auth_data = exp.get("auth") if isinstance(exp, dict) else {}
                pwd_hash = row.get("password_hash") or auth_data.get("password_hash")
                role = row.get("role") or auth_data.get("role", "candidate")
                inst = row.get("institution_name") or auth_data.get("institution_name", "IIT Madras")
                dept = auth_data.get("department", "Computer Science & Engineering")
                grad_yr = auth_data.get("graduation_year", 2026)

                user_record = {
                    "id": str(row["id"]),
                    "email": row["email"],
                    "user_name": row["user_name"] or "User",
                    "password_hash": pwd_hash,
                    "role": role,
                    "institution_name": inst,
                    "department": dept,
                    "graduation_year": grad_yr,
                    "skills": row.get("skills") or []
                }
                _LOCAL_USERS_DB[email_clean] = user_record
        except Exception as e:
            logger.warning(f"Supabase user lookup failed: {e}")

    if not user_record:
        raise ValueError("Invalid email or password.")

    if not verify_password(req.password, user_record.get("password_hash", "")):
        raise ValueError("Invalid email or password.")

    token = create_access_token({
        "sub": user_record["id"],
        "email": email_clean,
        "role": user_record.get("role", "candidate"),
        "name": user_record.get("user_name", "")
    })

    return AuthResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse(
            id=user_record["id"],
            email=email_clean,
            user_name=user_record.get("user_name", "User"),
            role=user_record.get("role", "candidate"),
            institution_name=user_record.get("institution_name"),
            department=user_record.get("department"),
            graduation_year=user_record.get("graduation_year"),
            skills=[]
        )
    )

def get_current_user(token: str) -> Optional[UserResponse]:
    payload = decode_access_token(token)
    if not payload:
        return None
    email = payload.get("email", "").lower()
    if email in _LOCAL_USERS_DB:
        u = _LOCAL_USERS_DB[email]
        return UserResponse(
            id=u["id"],
            email=u["email"],
            user_name=u["user_name"],
            role=u.get("role", "candidate"),
            institution_name=u.get("institution_name"),
            department=u.get("department"),
            graduation_year=u.get("graduation_year"),
            skills=[]
        )
    
    supabase = get_supabase()
    if supabase:
        try:
            resp = supabase.table("user_profiles").select("*").eq("email", email).execute()
            if resp.data:
                row = resp.data[0]
                exp = row.get("experience") or {}
                auth_data = exp.get("auth") if isinstance(exp, dict) else {}
                user_res = UserResponse(
                    id=str(row["id"]),
                    email=row["email"],
                    user_name=row["user_name"] or "User",
                    role=row.get("role") or auth_data.get("role", "candidate"),
                    institution_name=row.get("institution_name") or auth_data.get("institution_name", "Other Indian University / Institute"),
                    department=auth_data.get("department", "Computer Science & Engineering"),
                    graduation_year=auth_data.get("graduation_year", 2026),
                    skills=[]
                )
                _LOCAL_USERS_DB[email] = {
                    "id": user_res.id,
                    "email": user_res.email,
                    "user_name": user_res.user_name,
                    "role": user_res.role,
                    "institution_name": user_res.institution_name,
                    "department": user_res.department,
                    "graduation_year": user_res.graduation_year,
                    "skills": []
                }
                return user_res
        except Exception as e:
            logger.warning(f"Error fetching user from Supabase: {e}")
    return None

def update_user_profile(user_id: str, req: UserUpdateRequest) -> UserResponse:
    supabase = get_supabase()
    matched_email = None

    # Update local in-memory cache
    for em, u in _LOCAL_USERS_DB.items():
        if u.get("id") == user_id:
            matched_email = em
            if req.user_name is not None and req.user_name.strip():
                u["user_name"] = req.user_name.strip()
            if req.institution_name is not None and req.institution_name.strip():
                u["institution_name"] = req.institution_name.strip()
            if req.department is not None and req.department.strip():
                u["department"] = req.department.strip()
            if req.graduation_year is not None:
                u["graduation_year"] = req.graduation_year
            break

    # Update in Supabase
    if supabase:
        try:
            updates: Dict[str, Any] = {}
            if req.user_name is not None and req.user_name.strip():
                updates["user_name"] = req.user_name.strip()

            curr = supabase.table("user_profiles").select("*").eq("id", user_id).execute()
            if curr.data:
                row = curr.data[0]
                matched_email = row.get("email")
                exp = row.get("experience") or {}
                auth_data = exp.get("auth") if isinstance(exp, dict) else {}
                
                if req.institution_name is not None and req.institution_name.strip():
                    auth_data["institution_name"] = req.institution_name.strip()
                if req.department is not None and req.department.strip():
                    auth_data["department"] = req.department.strip()
                if req.graduation_year is not None:
                    auth_data["graduation_year"] = req.graduation_year

                exp["auth"] = auth_data
                updates["experience"] = exp
                updates["education"] = [{"degree": "B.Tech", "department": auth_data.get("department", "CSE"), "year": auth_data.get("graduation_year", 2026)}]
                
                supabase.table("user_profiles").update(updates).eq("id", user_id).execute()

                # Sync into local cache
                if matched_email:
                    _LOCAL_USERS_DB[matched_email] = {
                        "id": user_id,
                        "email": matched_email,
                        "user_name": updates.get("user_name", row.get("user_name", "User")),
                        "role": row.get("role") or auth_data.get("role", "candidate"),
                        "institution_name": auth_data.get("institution_name", req.institution_name),
                        "department": auth_data.get("department", req.department),
                        "graduation_year": auth_data.get("graduation_year", req.graduation_year),
                        "skills": row.get("skills") or []
                    }
        except Exception as e:
            logger.warning(f"Error updating user profile in Supabase: {e}")

    # Return refreshed user record
    if matched_email and matched_email in _LOCAL_USERS_DB:
        u = _LOCAL_USERS_DB[matched_email]
        return UserResponse(
            id=u["id"],
            email=u["email"],
            user_name=u["user_name"],
            role=u.get("role", "candidate"),
            institution_name=u.get("institution_name"),
            department=u.get("department"),
            graduation_year=u.get("graduation_year"),
            skills=[]
        )

    return UserResponse(
        id=user_id,
        email=matched_email or "user@careerpath.ai",
        user_name=req.user_name or "User",
        role="candidate",
        institution_name=req.institution_name or "Other Indian University / Institute",
        department=req.department or "Computer Science & Engineering",
        graduation_year=req.graduation_year or 2026,
        skills=[]
    )
