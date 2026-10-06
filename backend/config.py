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

settings = Settings()
