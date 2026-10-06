import re
from typing import Any, List, Dict
from fastapi import HTTPException

# Regex pattern for valid, safe email addresses (prevents PostgREST delimiter/operator injection)
EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

# Regex pattern for safe skills (alphanumeric, spaces, and safe tech symbols like C++, C#, .NET, CI/CD)
SKILL_PATTERN = re.compile(r"^[a-zA-Z0-9\s\+\#\.\-\/\&\_]{1,80}$")

# Disallowed SQL/NoSQL injection tokens and signatures
DANGEROUS_SQL_PATTERNS = [
    re.compile(r"(\bUNION\b\s+\bSELECT\b)", re.IGNORECASE),
    re.compile(r"(\bOR\b\s+['\"]?1['\"]?\s*=\s*['\"]?1)", re.IGNORECASE),
    re.compile(r"(\bDROP\b\s+\bTABLE\b)", re.IGNORECASE),
    re.compile(r"(\bINSERT\b\s+\bINTO\b)", re.IGNORECASE),
    re.compile(r"(\bDELETE\b\s+\bFROM\b)", re.IGNORECASE),
    re.compile(r"(\bEXEC\b\s*\(|\bEXECUTE\b\s*\()", re.IGNORECASE),
    re.compile(r"(--|/\*|\*/|;\s*$)", re.IGNORECASE),
    re.compile(r"(';\s*--)", re.IGNORECASE),
]

DANGEROUS_NOSQL_PATTERNS = [
    re.compile(r"(\$where|\$gt|\$lt|\$ne|\$regex|\$in|\$nin|\$all|\$expr)", re.IGNORECASE),
]

def sanitize_text(value: str, max_length: int = 500, field_name: str = "Input") -> str:
    """
    Sanitizes string inputs:
    - Removes null bytes
    - Enforces max length
    - Rejects SQL and NoSQL injection attack payloads
    """
    if not isinstance(value, str):
        raise ValueError(f"Invalid type for {field_name}: expected string, got {type(value).__name__}")

    # Strip null bytes
    cleaned = value.replace("\x00", "").strip()

    if len(cleaned) > max_length:
        raise ValueError(f"{field_name} exceeds maximum allowed length of {max_length} characters.")

    # Check for SQL injection patterns
    for pat in DANGEROUS_SQL_PATTERNS:
        if pat.search(cleaned):
            raise ValueError(f"Security Alert: Malicious SQL injection sequence detected in {field_name}.")

    # Check for NoSQL injection patterns
    for pat in DANGEROUS_NOSQL_PATTERNS:
        if pat.search(cleaned):
            raise ValueError(f"Security Alert: Malicious NoSQL operator sequence detected in {field_name}.")

    return cleaned

def sanitize_email(email: str) -> str:
    """
    Strictly validates and cleans email addresses.
    Prevents parameter pollution and PostgREST operator injection.
    """
    cleaned = sanitize_text(email, max_length=150, field_name="Email").lower()
    
    # Must not contain commas, quotes, parentheses, semicolons
    if any(char in cleaned for char in [",", "'", '"', "(", ")", ";", " "]):
        raise ValueError("Email address contains illegal characters.")

    if not EMAIL_PATTERN.match(cleaned):
        raise ValueError("Invalid email format. Please provide a standard address (e.g. name@domain.com).")

    return cleaned

def sanitize_identifier(id_val: str, field_name: str = "Identifier") -> str:
    """
    Ensures IDs are clean alphanumeric, integer, or UUID strings.
    """
    cleaned = sanitize_text(id_val, max_length=64, field_name=field_name)
    # Only allow alphanumeric, hyphens, and underscores (standard UUIDs / integers)
    if not re.match(r"^[a-zA-Z0-9\-_]+$", cleaned):
        raise ValueError(f"Invalid {field_name}: must be alphanumeric or standard UUID format.")
    return cleaned

def sanitize_skills_list(skills: List[str], max_count: int = 150) -> List[str]:
    """
    Sanitizes an entire list of skills, removing empty entries and verifying safety.
    """
    if not isinstance(skills, list):
        raise ValueError("Skills must be provided as a list.")

    if len(skills) > max_count:
        skills = skills[:max_count]

    sanitized = []
    seen = set()

    for s in skills:
        if not isinstance(s, str):
            continue
        cleaned = sanitize_text(s, max_length=80, field_name="Skill item")
        if not cleaned:
            continue
        if not SKILL_PATTERN.match(cleaned):
            continue
        
        lower = cleaned.lower()
        if lower not in seen:
            seen.add(lower)
            sanitized.append(cleaned)

    return sanitized
