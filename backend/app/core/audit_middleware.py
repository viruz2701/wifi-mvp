from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.tasks.audit import log_action
from app.core.config import settings
from jose import jwt, JWTError
from app.crud.user import user as crud_user
from app.db.session import SessionLocal

class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # Логируем только успешные запросы на изменение данных
        if response.status_code < 400 and request.method in ["POST", "PUT", "DELETE"]:
            user_id = None
            auth_header = request.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header[7:]
                try:
                    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
                    email = payload.get("sub")
                    if email:
                        db = SessionLocal()
                        try:
                            user = crud_user.get_by_email(db, email=email)
                            if user:
                                user_id = user.id
                        finally:
                            db.close()
                except JWTError:
                    pass  # Невалидный токен – игнорируем

            # Извлекаем тип ресурса из пути
            path_parts = request.url.path.split('/')
            resource_type = path_parts[3] if len(path_parts) > 3 else 'unknown'

            details = {
                "path": request.url.path,
                "method": request.method,
                "query_params": dict(request.query_params),
            }

            # Запускаем асинхронную задачу записи лога
            log_action.delay(
                user_id=user_id,
                action=request.method,
                resource_type=resource_type,
                resource_id=None,
                details=details,
                ip=request.client.host
            )

        return response