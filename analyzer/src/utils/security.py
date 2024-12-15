from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

from src.config import settings

API_KEY = settings.API_KEY
api_key_header = APIKeyHeader(name="X-API-Key")


def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or missing API key")