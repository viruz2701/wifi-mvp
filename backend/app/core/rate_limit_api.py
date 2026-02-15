import time
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.redis_client import get_redis

class APIRateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, calls_per_minute: int = 100):
        super().__init__(app)
        self.calls_per_minute = calls_per_minute

    async def dispatch(self, request: Request, call_next):
        # Не применяем к публичным эндпоинтам портала (уже есть свой)
        if request.url.path.startswith("/portal/"):
            return await call_next(request)

        client_ip = request.client.host
        redis = await get_redis()
        minute_key = f"rate:api:{client_ip}:{int(time.time() // 60)}"
        count = await redis.incr(minute_key)
        if count == 1:
            await redis.expire(minute_key, 60)

        if count > self.calls_per_minute:
            raise HTTPException(status_code=429, detail="Too many API requests from this IP")

        response = await call_next(request)
        return response