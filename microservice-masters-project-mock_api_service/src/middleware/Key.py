

from fastapi import  HTTPException, Security
from fastapi.security import APIKeyHeader
from starlette import status
from config import get_settings


api_key_header = APIKeyHeader(name="X-API-Key")
settings = get_settings()

def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    if api_key_header == settings.server.api_key:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )