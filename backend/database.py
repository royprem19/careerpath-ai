from supabase import create_client, Client
from .config import settings
import logging

logger = logging.getLogger(__name__)
_supabase_client = None

def get_supabase() -> Client | None:
    global _supabase_client
    if _supabase_client is None:
        key = settings.SUPABASE_SERVICE_KEY or settings.SUPABASE_ANON_KEY
        if settings.SUPABASE_URL and key:
            try:
                _supabase_client = create_client(settings.SUPABASE_URL, key)
                logger.info("Supabase client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Supabase client: {e}")
                return None
    return _supabase_client
