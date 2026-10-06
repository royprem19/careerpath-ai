import socket
import logging
from typing import Optional, Tuple
import httpx
from rapidfuzz.distance import DamerauLevenshtein

logger = logging.getLogger(__name__)

# Major authentic email providers worldwide and in India
MAJOR_EMAIL_DOMAINS = [
    "gmail.com",
    "googlemail.com",
    "yahoo.com",
    "yahoo.co.in",
    "yahoo.co.uk",
    "outlook.com",
    "hotmail.com",
    "live.com",
    "icloud.com",
    "proton.me",
    "protonmail.com",
    "rediffmail.com",
    "zoho.com",
    "aol.com"
]

# Explicit fast lookup for most frequent typos
KNOWN_TYPO_MAP = {
    # Gmail typos
    "gmai.com": "gmail.com",
    "gamil.com": "gmail.com",
    "gmial.com": "gmail.com",
    "gmaill.com": "gmail.com",
    "gmaii.com": "gmail.com",
    "gma.com": "gmail.com",
    "gmeil.com": "gmail.com",
    "gmail.co": "gmail.com",
    "gmail.cm": "gmail.com",
    "gmal.com": "gmail.com",
    "gemail.com": "gmail.com",
    "gimail.com": "gmail.com",
    "gmaul.com": "gmail.com",
    "googlemail.co": "googlemail.com",
    # Yahoo typos
    "yaho.com": "yahoo.com",
    "yahooo.com": "yahoo.com",
    "yaho.co": "yahoo.com",
    "yaho.in": "yahoo.co.in",
    "yhaoo.com": "yahoo.com",
    "yaho.co.in": "yahoo.co.in",
    "yahoo.co": "yahoo.com",
    # Microsoft / Hotmail / Outlook typos
    "hotmial.com": "hotmail.com",
    "hotmai.com": "hotmail.com",
    "hotamil.com": "hotmail.com",
    "hotmaill.com": "hotmail.com",
    "outlok.com": "outlook.com",
    "outloo.com": "outlook.com",
    "ootlook.com": "outlook.com",
    "putlook.com": "outlook.com",
    "outlook.co": "outlook.com",
    # Apple iCloud typos
    "icoud.com": "icloud.com",
    "iclod.com": "icloud.com",
    "icloud.co": "icloud.com",
    # Rediffmail typos
    "redifmail.com": "rediffmail.com",
    "redif.com": "rediffmail.com"
}

# Known disposable or temporary burner domains that shouldn't be used for academic/career credentials
DISPOSABLE_DOMAINS = {
    "tempmail.com", "10minutemail.com", "guerrillamail.com", 
    "mailinator.com", "throwawaymail.com", "yopmail.com", 
    "sharklasers.com", "nada.ltd", "getairmail.com", "fakeinbox.com"
}

def detect_domain_typo(domain: str) -> Optional[str]:
    """
    Checks if a domain is a misspelling of a major email provider.
    Returns the suggested canonical domain if a typo is found, else None.
    """
    domain = domain.lower().strip()
    
    # 1. Exact typo dictionary match
    if domain in KNOWN_TYPO_MAP:
        return KNOWN_TYPO_MAP[domain]
    
    if domain in MAJOR_EMAIL_DOMAINS:
        return None
        
    # 2. Fuzzy match against major domains (edit distance <= 1, or transposition distance == 2 with prefix match)
    for major in MAJOR_EMAIL_DOMAINS:
        dist = DamerauLevenshtein.distance(domain, major)
        if dist == 1:
            return major
        if dist == 2 and len(domain) >= 6 and domain[:3] == major[:3]:
            return major
            
    return None

def check_domain_dns_mx(domain: str) -> Tuple[bool, Optional[str]]:
    """
    Verifies that the domain exists and can receive email.
    Uses Google DNS over HTTPS for fast, non-blocking MX checking,
    with local socket DNS fallback.
    """
    domain = domain.lower().strip()

    # Fast path for known major domains
    if domain in MAJOR_EMAIL_DOMAINS:
        return True, None

    # Try DNS-over-HTTPS MX record lookup
    try:
        url = f"https://dns.google/resolve?name={domain}&type=MX"
        resp = httpx.get(url, timeout=2.5)
        if resp.status_code == 200:
            data = resp.json()
            status = data.get("Status")
            # Status 3 is NXDOMAIN (domain does not exist)
            if status == 3:
                return False, f"The domain '{domain}' does not exist (NXDOMAIN)."
            # If status == 0, check if Answer or Authority records exist
            if status == 0:
                answers = data.get("Answer", [])
                if answers:
                    return True, None
                # Check A record fallback if no direct MX (RFC 5321 allows mail to A record if no MX)
                a_url = f"https://dns.google/resolve?name={domain}&type=A"
                a_resp = httpx.get(a_url, timeout=2.0)
                if a_resp.status_code == 200 and a_resp.json().get("Answer"):
                    return True, None
    except Exception as e:
        logger.debug(f"DoH check failed for {domain}, falling back to socket: {e}")

    # Fallback to local socket DNS resolution
    try:
        socket.getaddrinfo(domain, None, proto=socket.IPPROTO_TCP)
        return True, None
    except socket.gaierror:
        return False, f"The domain '{domain}' could not be resolved by DNS."
    except Exception:
        # Graceful fail-open on network timeouts so offline development isn't blocked
        return True, None

def validate_email_domain(email: str) -> str:
    """
    Validates the domain of an email address:
    1. Rejects disposable/temporary email domains.
    2. Detects typos for major providers (e.g. gmai.com -> gmail.com).
    3. Verifies DNS existence for unfamiliar domains.
    
    Raises ValueError with a friendly, actionable error message if invalid.
    """
    if "@" not in email:
        raise ValueError("Invalid email address: missing '@' separator.")
        
    local_part, domain = email.strip().split("@", 1)
    domain = domain.lower().strip()
    
    if not domain or "." not in domain:
        raise ValueError("Invalid email domain format.")
        
    # Check disposable
    if domain in DISPOSABLE_DOMAINS:
        raise ValueError(f"Temporary or disposable email addresses ('{domain}') are not permitted. Please use a permanent email address.")
        
    # Check typos
    suggested = detect_domain_typo(domain)
    if suggested:
        raise ValueError(f"Invalid email domain '{domain}'. Did you mean '{suggested}'?")
        
    # Check DNS existence for non-major domains
    if domain not in MAJOR_EMAIL_DOMAINS:
        exists, err_msg = check_domain_dns_mx(domain)
        if not exists:
            raise ValueError(f"Cannot deliver to '{domain}': {err_msg}")
            
    return email.strip().lower()
