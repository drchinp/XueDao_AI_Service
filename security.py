from dotenv import load_dotenv
load_dotenv("/var/www/xuedao-ai-service/.env")
from fastapi import Header, HTTPException
import os

API_KEY = os.getenv("AI_SERVICE_KEY", "CHANGE_ME")

def verify_key(x_api_key: str = Header()):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
