import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import get_db
from app.db.base import Base
from app.core.config import settings

# Используем тестовую БД (должна существовать)
SQLALCHEMY_DATABASE_URL = "postgresql://wifi_user:wifi_pass@localhost:5432/wifi_auth_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    # Создаем таблицы перед тестами
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    # Очищаем после тестов
    Base.metadata.drop_all(bind=engine)