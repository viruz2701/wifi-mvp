from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.session import get_db
from app.crud.user import user as crud_user
from app.schemas.token import TokenData
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")   

async def get_current_user_optional(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User | None:
    try:
        return await get_current_user(db, token)
    except HTTPException:
        return None



async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = crud_user.get_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def get_current_superuser(current_user: User = Depends(get_current_active_user)) -> User:
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user

# Новые зависимости для ролей
async def get_current_admin(current_user: User = Depends(get_current_active_user)) -> User:
    if current_user.role != "admin" and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Admin role required")
    return current_user

async def get_current_marketing(current_user: User = Depends(get_current_active_user)) -> User:
    if current_user.role not in ["admin", "marketing"] and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Marketing role required")
    return current_user

async def get_current_venue_owner(current_user: User = Depends(get_current_active_user)) -> User:
    if current_user.role == "venue_owner" and current_user.venue_id:
        return current_user
    if current_user.is_superuser or current_user.role == "admin":
        return current_user
    raise HTTPException(status_code=403, detail="Venue owner or admin required")

async def get_current_venue_owner_or_admin(
    current_user: User = Depends(get_current_active_user)
) -> User:
    if current_user.is_superuser or current_user.role == "admin":
        return current_user
    if current_user.role == "venue_owner" and current_user.venue_id:
        return current_user
    raise HTTPException(status_code=403, detail="Not enough permissions")