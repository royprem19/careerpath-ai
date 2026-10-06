import os
from pathlib import Path
from dotenv import load_dotenv

# Ensure .env inside backend/ is loaded
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path)
load_dotenv()

class Settings:
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_ANON_KEY: str = os.getenv("SUPABASE_ANON_KEY", "")
    SUPABASE_SERVICE_KEY: str = os.getenv("SUPABASE_SERVICE_KEY", "")
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    JWT_SECRET: str = os.getenv("JWT_SECRET", "careerpath_ai_bharat_2026_super_secret_jwt_key_98234")
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:5173")

    # SMTP Email Configuration
    SMTP_HOST: str = os.getenv("SMTP_HOST", "")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    SMTP_FROM: str = os.getenv("SMTP_FROM", os.getenv("SMTP_USER", "noreply@careerpath.ai"))
    SMTP_TLS: bool = os.getenv("SMTP_TLS", "true").lower() in ("true", "1", "yes")

settings = Settings()
