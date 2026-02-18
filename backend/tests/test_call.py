import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from app.main import app
from app.models.sms_provider import SMSProvider, SMSProviderType
from app.db.session import get_db
from tests.conftest import override_get_db, TestingSessionLocal

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture
def mock_call_provider():
    with patch('app.api.v1.endpoints.call_auth.get_call_provider') as mock:
        adapter = AsyncMock()
        adapter.initiate_call.return_value = {
            "call_id": "test_call_id",
            "confirmation_number": "12345",
            "qr_code_uri": "http://example.com/qr"
        }
        mock.return_value = adapter
        yield mock

def test_call_request(mock_call_provider):
    # Создаём тестового провайдера
    db = TestingSessionLocal()
    provider = SMSProvider(
        name="Test Call",
        type=SMSProviderType.CALLPASSWORD,
        config={"api_key": "test", "api_secret": "test"},
        is_active=True
    )
    db.add(provider)
    db.commit()
    db.close()

    response = client.post("/api/v1/auth/call/request", json={
        "phone": "+375291234567",
        "mac": "AA:BB:CC:DD:EE:FF",
        "venue_id": 1
    })
    assert response.status_code == 200
    data = response.json()
    assert "call_id" in data
    assert "confirmation_number" in data