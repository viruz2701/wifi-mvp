import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import get_db
from tests.conftest import override_get_db, TestingSessionLocal

client = TestClient(app)
app.dependency_overrides[get_db] = override_get_db

def test_opennds_auth_page():
    response = client.get("/api/v1/portal/opennds?clientip=192.168.1.100&gatewayname=test.com&tok=12345")
    assert response.status_code == 200
    assert "Добро пожаловать" in response.text

def test_opennds_auth_request(mocker):
    # Мокаем отправку SMS
    mocker.patch('app.api.v1.endpoints.opennds.get_sms_provider_by_type', return_value=None)
    mocker.patch('app.api.v1.endpoints.opennds.get_sms_adapter', return_value=AsyncMock())

    response = client.post("/api/v1/portal/opennds/auth", data={
        "tok": "12345",
        "clientip": "192.168.1.100",
        "phone": "+375291234567"
    })
    assert response.status_code == 302  # redirect
    assert "/api/v1/portal/opennds/verify" in response.headers["location"]