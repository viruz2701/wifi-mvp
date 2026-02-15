from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.tasks.audit import log_action
from app.core.dependencies import get_current_user_optional

class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # Логируем только успешные запросы на изменение данных
        if response.status_code < 400 and request.method in ["POST", "PUT", "DELETE"]:
            # Пытаемся получить текущего пользователя (может быть None)
            user = await get_current_user_optional(request)
            user_id = user.id if user else None

            # Извлекаем тип ресурса из пути (упрощённо)
            path_parts = request.url.path.split('/')
            resource_type = path_parts[3] if len(path_parts) > 3 else 'unknown'

            # Собираем детали (можно расширить)
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
                resource_id=None,  # можно попытаться извлечь из path
                details=details,
                ip=request.client.host
            )

        return response