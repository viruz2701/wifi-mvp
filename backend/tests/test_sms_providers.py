# backend/tests/test_sms_providers.py
import pytest
from unittest.mock import AsyncMock, patch
from app.core.sms import WebSmsAdapter

@pytest.mark.asyncio
async def test_websms_send_success():
    config = {"user": "test", "apikey": "key", "sender": "Test"}
    adapter = WebSmsAdapter(config)
    
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": True, "id": 12345}
    
    with patch("httpx.AsyncClient.get", return_value=mock_response) as mock_get:
        result = await adapter.send("+375291234567", "Test message")
        assert result is True
        mock_get.assert_called_once()
        # Проверяем, что номер отправлен без плюса
        called_params = mock_get.call_args[1]["params"]
        assert called_params["phone"] == "375291234567"

@pytest.mark.asyncio
async def test_websms_send_error():
    config = {"user": "test", "apikey": "key"}
    adapter = WebSmsAdapter(config)
    
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": False, "code": 4, "message": "Invalid API key"}
    
    with patch("httpx.AsyncClient.get", return_value=mock_response):
        result = await adapter.send("+375291234567", "Test")
        assert result is False