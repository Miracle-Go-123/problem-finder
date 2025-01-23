from fastapi import HTTPException, Security
from fastapi.security import api_key
from dotenv import load_dotenv
import os

load_dotenv()

api_key_header = api_key.APIKeyHeader(name="X_API_KEY")

async def validate_api_key(key: str = Security(api_key_header)):
    if key != os.getenv("NEXT_API_KEY"):
        raise HTTPException(status_code=401, detail="Unauthorized Call")
    