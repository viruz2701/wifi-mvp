from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app.db.session import get_db
from app.crud.user import user as crud_user
from app.schemas.user import UserCreate, UserOut
from app.schemas.token import Token
from app.core.security import create_access_token
from app.core.config import settings

router = APIRouter()

@router.post("/register", response_model=UserOut)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    # Проверяем, есть ли уже пользователи
    existing_users = db.query(crud_user.model).count()
    if existing_users > 0:
        raise HTTPException(status_code=403, detail="Registration is closed. First user already created.")
    # Создаём первого пользователя с правами суперпользователя
    user_in.is_superuser = True
    user = crud_user.create(db, obj_in=user_in)
    return user

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud_user.authenticate(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}