from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY_NAME = "X_API_KEY"
API_KEY = os.getenv("NEXT_API_KEY")

class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        excluded_paths = ["/"]
        if request.url.path not in excluded_paths:
            api_key = request.headers.get(API_KEY_NAME)
            if api_key != API_KEY:
                return Response("Unauthorized Call", status_code=401)
        return await call_next(request)

