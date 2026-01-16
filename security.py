from fastapi import Header, HTTPException
import os

API_KEY = os.getenv("AI_SERVICE_KEY")

def verify_key(x_api_key: str = Header(None, alias="X-API-Key")):
    if not API_KEY:
        raise HTTPException(
            status_code=500,
            detail="Server misconfiguration: AI_SERVICE_KEY not set"
        )
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key"
        )
