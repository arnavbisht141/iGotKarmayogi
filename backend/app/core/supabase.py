"""
Supabase Client Singleton & Helpers for iGOT Karmayogi Backend
Provides standard and administrative Supabase client instances.
"""

from typing import Optional
from supabase import create_client, Client
from app.core.config import settings

_supabase_client: Optional[Client] = None
_supabase_admin_client: Optional[Client] = None


def get_supabase_client() -> Optional[Client]:
    """
    Returns the standard public / anon Supabase client.
    Returns None if SUPABASE_URL or SUPABASE_KEY is not configured.
    """
    global _supabase_client
    if _supabase_client is None and settings.SUPABASE_URL and settings.SUPABASE_KEY:
        try:
            _supabase_client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        except Exception as e:
            print(f"Warning: Failed to initialize Supabase client: {e}")
            return None
    return _supabase_client


def get_supabase_admin_client() -> Optional[Client]:
    """
    Returns the privileged service-role Supabase client for administrative workflows.
    Returns None if SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY is not configured.
    """
    global _supabase_admin_client
    key = settings.SUPABASE_SERVICE_ROLE_KEY or settings.SUPABASE_KEY
    if _supabase_admin_client is None and settings.SUPABASE_URL and key:
        try:
            _supabase_admin_client = create_client(settings.SUPABASE_URL, key)
        except Exception as e:
            print(f"Warning: Failed to initialize Supabase admin client: {e}")
            return None
    return _supabase_admin_client
