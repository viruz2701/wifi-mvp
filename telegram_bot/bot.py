import asyncio
import logging
import os
import redis.asyncio as redis
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
import httpx

logging.basicConfig(level=logging.INFO)

async def load_telegram_settings():
    """Загружает настройки Telegram-бота из внутреннего эндпоинта бэкенда."""
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get("http://backend:8000/api/v1/internal/telegram-settings", timeout=5)
            resp.raise_for_status()
            data = resp.json()
            return (
                data.get("telegram_bot_token"),
                data.get("telegram_bot_username"),
                data.get("telegram_bot_webhook_url")
            )
        except Exception as e:
            logging.error(f"Failed to load settings from backend: {e}")
            # fallback на переменные окружения
            return (
                os.getenv("TELEGRAM_BOT_TOKEN"),
                os.getenv("TELEGRAM_BOT_USERNAME"),
                os.getenv("TELEGRAM_BOT_WEBHOOK_URL")
            )

async def main():
    # Загружаем настройки
    token, username, webhook_url = await load_telegram_settings()
    if not token:
        raise ValueError("Telegram bot token not configured")

    bot = Bot(token=token)
    dp = Dispatcher()
    redis_client = redis.Redis(
        host=os.getenv("REDIS_HOST", "redis"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        db=int(os.getenv("REDIS_DB", 1)),
        decode_responses=True
    )

    contact_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Поделиться номером телефона", request_contact=True)]
        ],
        resize_keyboard=True
    )

    @dp.message(CommandStart())
    async def start_command(message: Message):
        args = message.text.split()
        state = args[1] if len(args) > 1 else None
        if not state:
            await message.answer("Пожалуйста, используйте ссылку из личного кабинета Wi-Fi.")
            return

        chat_id = str(message.chat.id)
        # Сохраняем chat_id -> state для обратного поиска при получении контакта
        await redis_client.setex(f"tg:chat:{chat_id}", 300, state)
        # НЕ перезаписываем tg:init:{state} – он уже создан бэкендом и содержит mac:venue_id

        await message.answer(
            "Нажмите кнопку ниже, чтобы поделиться номером телефона и войти в Wi-Fi.",
            reply_markup=contact_keyboard
        )

    @dp.message(lambda message: message.contact is not None)
    async def handle_contact(message: Message):
        contact = message.contact
        phone = contact.phone_number
        if phone.startswith('+'):
            phone = phone[1:]  # убираем +

        state = await redis_client.get(f"tg:chat:{message.chat.id}")
        if not state:
            await message.answer("Сессия устарела. Пожалуйста, начните заново на портале.")
            return

        async with httpx.AsyncClient() as client:
            try:
                resp = await client.post(
                    "http://backend:8000/api/v1/auth/telegram/callback",
                    json={
                        "state": state,
                        "phone": phone,
                        "chat_id": message.chat.id
                    },
                    timeout=5
                )
                if resp.status_code == 200:
                    await message.answer("✅ Авторизация успешна! Можете закрыть Telegram и продолжить в браузере.")
                    # Очищаем ключи
                    await redis_client.delete(f"tg:chat:{message.chat.id}")
                    # Ключ tg:init:{state} удалит бэкенд при успешном callback
                else:
                    await message.answer("❌ Ошибка авторизации. Попробуйте ещё раз.")
            except Exception as e:
                logging.error(f"Error sending to backend: {e}")
                await message.answer("Сервис временно недоступен. Попробуйте позже.")

    async def on_startup():
        # Удаляем вебхук на старте (на всякий случай)
        await bot.delete_webhook()
        logging.info("Webhook removed, starting polling")

    async def on_shutdown():
        await redis_client.close()
        await bot.session.close()

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())