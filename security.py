from fastapi import Header, HTTPException
import os

API_KEY = os.getenv("AI_SERVICE_KEY")

def verify_key(x_api_key: str = Header(None)):
    if not API_KEY:
        raise HTTPException(
            status_code=500,
            detail="Server API key not configured (AI_SERVICE_KEY missing)"
        )

    if not x_api_key or x_api_key != API_KEY:
        raise HTTPException(
            status_code=403,
            detail="Invalid or missing API key"
        )
