from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from app.api.v1.endpoints import (
    auth, users, venues, nas_devices, test,
    sms_providers, sms_auth, local_auth, radius,
    user_profiles, sessions, local_users, netflow,
    wireguard, portal_preview, portal_templates, banners,
    reports, export, call_auth, telegram_auth, opennds,
    builtin_templates,  # добавлен импорт для предустановленных шаблонов
    portal,  # <-- ДОБАВЛЕНО
)
from app.core.rate_limit import RateLimitMiddleware
from app.core.rate_limit_api import APIRateLimitMiddleware
from app.core.audit_middleware import AuditMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from app.api.v1.endpoints import settings as settings_router
from app.api.v1.endpoints import internal
from app.api.v1.endpoints import nas_status


app = FastAPI(title="WiFi Auth Platform MVP", version="0.2.0")

# CORS middleware (для разработки)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Кастомные middleware
app.add_middleware(RateLimitMiddleware, calls_per_minute=60)
app.add_middleware(APIRateLimitMiddleware, calls_per_minute=100)
app.add_middleware(AuditMiddleware)

# Подключаем все роутеры
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(venues.router, prefix="/api/v1/venues", tags=["venues"])
app.include_router(nas_devices.router, prefix="/api/v1/nas-devices", tags=["nas_devices"])
app.include_router(test.router, prefix="/api/v1", tags=["test"])
app.include_router(settings_router.router, prefix="/api/v1/settings", tags=["settings"])
app.include_router(internal.router, prefix="/api/v1", tags=["internal"])
app.include_router(sms_providers.router, prefix="/api/v1/sms-providers", tags=["sms_providers"])
app.include_router(sms_auth.router, prefix="/api/v1/auth", tags=["sms_auth"])
app.include_router(local_auth.router, prefix="/api/v1/auth", tags=["local_auth"])
app.include_router(radius.router, prefix="/api/v1/radius", tags=["radius"])
app.include_router(user_profiles.router, prefix="/api/v1/user-profiles", tags=["user_profiles"])
app.include_router(sessions.router, prefix="/api/v1/sessions", tags=["sessions"])
app.include_router(local_users.router, prefix="/api/v1/local-users", tags=["local_users"])
app.include_router(call_auth.router, prefix="/api/v1/auth", tags=["call_auth"])
app.include_router(telegram_auth.router, prefix="/api/v1/auth", tags=["telegram"])
app.include_router(opennds.router, prefix="/api/v1/portal", tags=["opennds"])
app.include_router(builtin_templates.router, prefix="/api/v1", tags=["builtin"])
app.include_router(netflow.router, prefix="/api/v1/netflow", tags=["netflow"])
app.include_router(wireguard.router, prefix="/api/v1/wireguard/peers", tags=["wireguard"])
app.include_router(portal_preview.router, prefix="/api/v1/portal", tags=["portal_preview"])
app.include_router(portal_templates.router, prefix="/api/v1/portal-templates", tags=["portal_templates"])
app.include_router(banners.router, prefix="/api/v1/banners", tags=["banners"])
app.include_router(reports.router, prefix="/api/v1/reports", tags=["reports"])
app.include_router(export.router, prefix="/api/v1/export", tags=["export"])
app.include_router(nas_status.router, prefix="/api/v1", tags=["nas"])



# <-- ДОБАВЛЕН РОУТЕР ПОРТАЛА
app.include_router(portal.router, prefix="/portal", tags=["portal"])

# Метрики Prometheus
Instrumentator().instrument(app).expose(app)

@app.get("/")
def root():
    return {"message": "WiFi Auth Platform API"}