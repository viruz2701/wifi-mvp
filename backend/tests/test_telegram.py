import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from app.main import app
from app.core.redis_client import get_redis
from app.db.session import get_db
from tests.conftest import override_get_db, TestingSessionLocal

client = TestClient(app)
app.dependency_overrides[get_db] = override_get_db

@pytest.mark.asyncio
async def test_telegram_init():
    response = client.post("/api/v1/auth/telegram/init", json={
        "mac": "AA:BB:CC:DD:EE:FF",
        "venue_id": 1
    })
    assert response.status_code == 200
    data = response.json()
    assert "state" in data
    assert "bot_link" in data

@pytest.mark.asyncio
async def test_telegram_callback():
    # Предварительно сохраняем state в Redis
    redis = await get_redis()
    await redis.setex("tg:init:teststate", 300, "AA:BB:CC:DD:EE:FF|1")

    response = client.post("/api/v1/auth/telegram/callback", json={
        "state": "teststate",
        "phone": "+375291234567",
        "chat_id": 12345
    })
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}