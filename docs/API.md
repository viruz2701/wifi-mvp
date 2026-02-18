# API документация

## Новые эндпоинты в Этапе 0

### Тарифы и площадки
- `GET /api/v1/venues/{id}/tariffs` – список тарифов, доступных на площадке.
- `POST /api/v1/venues/{id}/tariffs` – привязка тарифа к площадке (требует `tariff_id`, `priority`, `is_available`).
- `DELETE /api/v1/venues/{id}/tariffs/{tariff_id}` – удаление связи.

### Встроенные шаблоны портала
- `GET /builtin-templates` – список предустановленных шаблонов.
- `POST /builtin-templates/{id}/import?venue_id=...` – импорт шаблона для площадки.

### Rate limiting
Для эндпоинтов `/call/*`, `/telegram/*`, `/hotel/*` введены ограничения:
- `/call/request` – 10 запросов в минуту с одного IP.
- Остальные – 5 запросов в минуту.

## Обновлённые эндпоинты
- `/api/v1/auth/sms/request` – теперь требует валидацию номера телефона.
- `/api/v1/radius/authorize` – возвращает атрибуты тарифа.