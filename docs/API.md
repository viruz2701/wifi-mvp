API.md – описание эндпоинтов
markdown
# API документация WiFi Auth Platform

Полная документация API доступна в интерактивном формате Swagger по адресу:

**`/api/v1/docs`** (например, `http://localhost:8000/api/v1/docs`)

Swagger предоставляет возможность тестировать эндпоинты прямо в браузере и содержит детальные схемы запросов и ответов.

## Основные группы эндпоинтов

| Префикс                | Описание |
|------------------------|----------|
| `/api/v1/auth`         | Аутентификация (вход, регистрация, SMS-авторизация) |
| `/api/v1/users`        | Управление администраторами |
| `/api/v1/venues`       | Площадки |
| `/api/v1/nas-devices`  | NAS-устройства |
| `/api/v1/portal-templates` | Шаблоны портала |
| `/api/v1/banners`      | Баннеры |
| `/api/v1/user-profiles` | Профили Wi-Fi пользователей |
| `/api/v1/sessions`     | Сессии |
| `/api/v1/reports`      | Отчёты |
| `/api/v1/export`       | Экспорт данных (сессии, логи авторизаций) |
| `/api/v1/radius`       | Внутренние эндпоинты для RADIUS-сервера |
| `/api/v1/wireguard/peers` | Управление WireGuard пирами |
| `/api/v1/netflow/records` | Приём NetFlow записей (используется слушателем) |

## Аутентификация

Большинство эндпоинтов требуют JWT-токен, который передаётся в заголовке:
Authorization: Bearer <token>

text

Токен получается при вызове `POST /api/v1/auth/login` с логином и паролем администратора.

## Примеры запросов

### Получение списка площадок
```bash
curl -X GET http://localhost/api/v1/venues \
  -H "Authorization: Bearer <токен>"
Создание площадки
bash
curl -X POST http://localhost/api/v1/venues \
  -H "Authorization: Bearer <токен>" \
  -H "Content-Type: application/json" \
  -d '{"name":"Новая площадка", "domain":"cafe.example.com"}'
Экспорт сессий в CSV
bash
curl -X GET "http://localhost/api/v1/export/user-sessions?from_date=2026-01-01&to_date=2026-02-15&format=csv" \
  -H "Authorization: Bearer <токен>" \
  --output sessions.csv
Более подробную информацию о каждом эндпоинте, включая все параметры, типы данных и возможные ошибки, смотрите в Swagger.

text

После создания этих файлов выполните:

```bash
git add docs/
git commit -m "docs: add installation guide, user guide and API overview"
git push origin main