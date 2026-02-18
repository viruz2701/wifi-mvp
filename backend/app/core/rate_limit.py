import time
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.redis_client import get_redis

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware для ограничения запросов к порталу (/portal/*)."""
    def __init__(self, app, calls_per_minute: int = 60):
        super().__init__(app)
        self.calls_per_minute = calls_per_minute

    async def dispatch(self, request: Request, call_next):
        # Применяем только к путям, начинающимся с /portal/
        if not request.url.path.startswith("/portal/"):
            return await call_next(request)

        client_ip = request.client.host
        redis = await get_redis()
        minute_key = f"rate:ip:{client_ip}:{int(time.time() // 60)}"
        count = await redis.incr(minute_key)
        if count == 1:
            await redis.expire(minute_key, 60)

        if count > self.calls_per_minute:
            raise HTTPException(status_code=429, detail="Too many requests from this IP")

        response = await call_next(request)
        return response

class APIRateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware для ограничения запросов к API (/api/*)."""
    def __init__(self, app, default_calls_per_minute: int = 100):
        super().__init__(app)
        self.default_calls_per_minute = default_calls_per_minute
        # Специфические лимиты для путей
        self.limit_overrides = {
            "/api/v1/auth/call/request": 10,
            "/api/v1/auth/call/": 5,          # все остальные /call/*
            "/api/v1/auth/telegram/": 5,
            "/api/v1/auth/hotel/": 5,
        }

    async def dispatch(self, request: Request, call_next):
        # Не применяем к публичным эндпоинтам портала (уже есть свой)
        if request.url.path.startswith("/portal/"):
            return await call_next(request)

        # Определяем лимит для данного пути
        limit = self.default_calls_per_minute
        for path, custom_limit in self.limit_overrides.items():
            if request.url.path.startswith(path):
                limit = custom_limit
                break

        client_ip = request.client.host
        redis = await get_redis()
        minute_key = f"rate:api:{client_ip}:{int(time.time() // 60)}"
        count = await redis.incr(minute_key)
        if count == 1:
            await redis.expire(minute_key, 60)

        if count > limit:
            raise HTTPException(status_code=429, detail="Too many API requests from this IP")

        response = await call_next(request)
        return response