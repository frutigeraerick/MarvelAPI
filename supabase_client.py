import os
from typing import Optional
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET", "Marvel")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL and SUPABASE_KEY else None

def upload_image_to_supabase(file_bytes: bytes, dest_path: str, content_type: str = "image/jpeg") -> Optional[str]:

    if not supabase:
        return None
    try:
        supabase.storage.from_(SUPABASE_BUCKET).upload(dest_path, file_bytes, {"content-type": content_type})

        public_url = supabase.storage.from_(SUPABASE_BUCKET).get_public_url(dest_path)
        return public_url
    except Exception as e:
        print("Error subiendo a Supabase:", e)
        return None
