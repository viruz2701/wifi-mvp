from fastapi import FastAPI
from app.api.v1.endpoints import (
    auth, users, venues, nas_devices, test,
    sms_providers, sms_auth, local_auth, radius,
    user_profiles, sessions, local_users
)
from app.api.v1.endpoints import netflow
app = FastAPI(title="WiFi Auth Platform MVP", version="0.2.0")  # обновим версию

from app.api.v1.endpoints import wireguard
app.include_router(wireguard.router, prefix="/api/v1/wireguard/peers", tags=["wireguard"])

# Подключаем роутеры


app.include_router(netflow.router, prefix="/api/v1/netflow", tags=["netflow"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(venues.router, prefix="/api/v1/venues", tags=["venues"])
app.include_router(nas_devices.router, prefix="/api/v1/nas-devices", tags=["nas_devices"])
app.include_router(test.router, prefix="/api/v1", tags=["test"])

# Новые роутеры этапа 2
app.include_router(sms_providers.router, prefix="/api/v1/sms-providers", tags=["sms_providers"])
app.include_router(sms_auth.router, prefix="/api/v1/auth", tags=["sms_auth"])
app.include_router(local_auth.router, prefix="/api/v1/auth", tags=["local_auth"])
app.include_router(radius.router, prefix="/api/v1/radius", tags=["radius"])
app.include_router(user_profiles.router, prefix="/api/v1/user-profiles", tags=["user_profiles"])
app.include_router(sessions.router, prefix="/api/v1/sessions", tags=["sessions"])
app.include_router(local_users.router, prefix="/api/v1/local-users", tags=["local_users"])

@app.get("/")
def root():
    return {"message": "WiFi Auth Platform API"}