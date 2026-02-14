import time
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from app.core.redis_client import get_redis

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, calls_per_minute: int = 60):
        super().__init__(app)
        self.calls_per_minute = calls_per_minute

    async def dispatch(self, request: Request, call_next):
        # Применяем только к путям, начинающимся с /portal/
        if not request.url.path.startswith("/portal/"):
            return await call_next(request)

        client_ip = request.client.host
        redis = await get_redis()
        # Ключ с точностью до минуты
        minute_key = f"rate:ip:{client_ip}:{int(time.time() // 60)}"
        count = await redis.incr(minute_key)
        if count == 1:
            await redis.expire(minute_key, 60)  # живёт 60 секунд

        if count > self.calls_per_minute:
            # Превышен лимит
            raise HTTPException(status_code=429, detail="Too many requests from this IP")

        response = await call_next(request)
        return response