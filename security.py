from fastapi import Header, HTTPException
import os

API_KEY = os.getenv("AI_SERVICE_KEY")

def verify_key(
    x_api_key: str = Header(None, alias="X-API-Key")
):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="Server API key not configured")

    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
