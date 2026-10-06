import os
import sys
import uuid
from pathlib import Path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from datetime import datetime, timedelta, timezone
from fastapi.testclient import TestClient
from backend.main import app
from backend.services import auth_service

client = TestClient(app)

print("==================================================================")
print("CAREERPATH AI - EMAIL VERIFICATION & AUTH LIFECYCLE TEST SUITE")
print("==================================================================")

# 1. Invalid email format -> registration rejected
r_invalid_email = client.post("/api/auth/register", json={
    "email": "not-an-email",
    "password": "Password@123",
    "user_name": "Test User"
})
assert r_invalid_email.status_code in [400, 422], f"Expected 400/422 for invalid email, got {r_invalid_email.status_code}"
print("1.  [PASS] Invalid email format rejected on registration (Status:", r_invalid_email.status_code, ")")

# 1b. Typo email domain (e.g. gmai.com instead of gmail.com) -> registration rejected with suggestion
r_typo_email = client.post("/api/auth/register", json={
    "email": "roypremt0219@gmai.com",
    "password": "Password@123",
    "user_name": "Prem Roy"
})
assert r_typo_email.status_code in [400, 422], f"Expected 400/422 for typo domain, got {r_typo_email.status_code}: {r_typo_email.text}"
assert "gmail.com" in r_typo_email.text, f"Expected suggestion for gmail.com, got {r_typo_email.text}"
print("1b. [PASS] Typo domain 'gmai.com' correctly rejected with suggestion: '", r_typo_email.json().get("detail"), "'")

# 2. Register valid email -> Account created with emailVerified = False
test_email = f"test_candidate_{uuid.uuid4().hex[:6]}@you.com"
r_reg = client.post("/api/auth/register", json={
    "email": test_email,
    "password": "SecurePassword123",
    "user_name": "Vansh Chauhan",
    "role": "candidate",
    "institution_name": "Chandigarh University",
    "department": "Computer Science & Engineering",
    "graduation_year": 2028
})
assert r_reg.status_code == 200, f"Registration failed: {r_reg.text}"
reg_data = r_reg.json()
assert reg_data.get("email_verified") is False, "Newly registered user should NOT be verified!"
assert "access_token" not in reg_data, "Newly registered user MUST NOT receive a JWT access token!"
print("2. [PASS] User registered with email_verified = False (No JWT issued)")

# 3. Unverified user attempts login -> MUST FAIL (403 Forbidden)
r_login_unverified = client.post("/api/auth/login", json={
    "email": test_email,
    "password": "SecurePassword123"
})
assert r_login_unverified.status_code == 403, f"Expected 403, got {r_login_unverified.status_code}: {r_login_unverified.text}"
assert "verify your email" in r_login_unverified.json().get("detail", "").lower()
print("3. [PASS] Unverified user login blocked with 403: '", r_login_unverified.json().get("detail"), "'")

# 4. Unverified user attempting to access protected route (/api/auth/me) -> rejected with 401
r_protected = client.get("/api/auth/me")
assert r_protected.status_code == 401
print("4. [PASS] Unauthenticated access to protected route blocked (401)")

# 5. Extract verification token for testing
active_token = None
for tok, data in auth_service._VERIFICATION_TOKENS.items():
    if data.get("email") == test_email and not data.get("used"):
        active_token = tok
        break
assert active_token is not None, "Verification token was not created in auth_service!"
print("5. [PASS] Verification token created securely (Token length:", len(active_token), "chars)")

# 6. Test tampered/invalid token -> MUST FAIL (400)
r_tampered = client.get(f"/api/auth/verify-email?token={active_token}_tampered")
assert r_tampered.status_code == 400
print("6. [PASS] Tampered verification token rejected (400 Bad Request)")

import uuid
# 7. Test expired token -> MUST FAIL (400)
expired_token = auth_service.create_verification_token("expired_test@test.com", str(uuid.uuid4()))
auth_service._VERIFICATION_TOKENS[expired_token]["expires_at"] = datetime.now(timezone.utc) - timedelta(minutes=5)
r_expired = client.get(f"/api/auth/verify-email?token={expired_token}")
assert r_expired.status_code == 400
assert "expired" in r_expired.json().get("detail", "").lower()
print("7. [PASS] Expired verification token rejected (400 Bad Request)")

# 8. Test Resend Verification endpoint -> Generates new token & enforces cooldown
r_resend_cooldown = client.post("/api/auth/resend-verification", json={"email": test_email})
assert r_resend_cooldown.status_code == 429 or "wait" in r_resend_cooldown.text.lower()
print("8. [PASS] Resend verification cooldown enforced (Rate limit protection)")

# 9. Verify valid token -> Account becomes verified
r_verify = client.get(f"/api/auth/verify-email?token={active_token}")
assert r_verify.status_code == 200, f"Verification failed: {r_verify.text}"
assert r_verify.json().get("success") is True
print("9. [PASS] Valid verification token activated account successfully")

# 10. Already-used token -> MUST FAIL (400)
r_already_used = client.get(f"/api/auth/verify-email?token={active_token}")
assert r_already_used.status_code == 400
assert "already been used" in r_already_used.json().get("detail", "").lower()
print("10. [PASS] Already-used token rejected (Single-use enforcement)")

# 11. Login after verification -> SUCCEEDS and issues authenticated JWT
r_login_verified = client.post("/api/auth/login", json={
    "email": test_email,
    "password": "SecurePassword123"
})
assert r_login_verified.status_code == 200, f"Login after verification failed: {r_login_verified.text}"
login_data = r_login_verified.json()
jwt_token = login_data["access_token"]
user_data = login_data["user"]
assert user_data["email_verified"] is True
print("11. [PASS] Verified user successfully logged in and received JWT token")

# 12. Verified user accesses protected route with JWT -> SUCCEEDS
r_me = client.get("/api/auth/me", headers={"Authorization": f"Bearer {jwt_token}"})
assert r_me.status_code == 200
assert r_me.json()["email"] == test_email
print("12. [PASS] Authenticated request to /api/auth/me succeeded for:", r_me.json()["email"])

print("==================================================================")
print("ALL 12 EMAIL VERIFICATION & AUTH LIFECYCLE TESTS PASSED!")
print("==================================================================")
