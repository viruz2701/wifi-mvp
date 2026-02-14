def test_register_first_user(client):
    response = client.post("/api/v1/auth/register", json={
        "email": "admin@example.com",
        "password": "secret",
        "is_superuser": True,
        "role": "admin"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "admin@example.com"
    assert "id" in data

def test_register_second_user_fails(client):
    # Сначала создаем первого
    client.post("/api/v1/auth/register", json={
        "email": "admin@example.com",
        "password": "secret"
    })
    # Пытаемся создать второго
    response = client.post("/api/v1/auth/register", json={
        "email": "user2@example.com",
        "password": "secret"
    })
    assert response.status_code == 403

def test_login(client):
    # Регистрируем пользователя
    client.post("/api/v1/auth/register", json={
        "email": "test@example.com",
        "password": "testpass"
    })
    # Логинимся
    response = client.post("/api/v1/auth/login", data={
        "username": "test@example.com",
        "password": "testpass"
    })
    assert response.status_code == 200
    token = response.json()
    assert "access_token" in token