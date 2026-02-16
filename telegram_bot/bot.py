import asyncio
import logging
import redis.asyncio as redis
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
import httpx
from config import BOT_TOKEN, BACKEND_URL, REDIS_HOST, REDIS_PORT, REDIS_DB, WEBHOOK_FULL

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

# Клавиатура с запросом номера телефона
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
    # Сохраняем state -> chat_id и обратно
    await redis_client.setex(f"tg:state:{state}", 300, chat_id)
    await redis_client.setex(f"tg:chat:{chat_id}", 300, state)
    
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
    
    # Получаем state по chat_id
    state = await redis_client.get(f"tg:chat:{message.chat.id}")
    if not state:
        await message.answer("Сессия устарела. Пожалуйста, начните заново на портале.")
        return
    
    # Отправляем данные на бэкенд
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(BACKEND_URL, json={
                "state": state,
                "phone": phone,
                "chat_id": message.chat.id
            }, timeout=5)
            if resp.status_code == 200:
                await message.answer("✅ Авторизация успешна! Можете закрыть Telegram и продолжить в браузере.")
                # Очищаем ключи
                await redis_client.delete(f"tg:state:{state}")
                await redis_client.delete(f"tg:chat:{message.chat.id}")
            else:
                await message.answer("❌ Ошибка авторизации. Попробуйте ещё раз.")
        except Exception as e:
            logging.error(f"Error sending to backend: {e}")
            await message.answer("Сервис временно недоступен. Попробуйте позже.")

async def on_startup():
    await bot.set_webhook(url=WEBHOOK_FULL)
    logging.info(f"Webhook set to {WEBHOOK_FULL}")

async def on_shutdown():
    await bot.delete_webhook()
    await redis_client.close()

async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
    from aiohttp import web
    
    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host='0.0.0.0', port=8080)
    await site.start()
    
    logging.info("Bot started with webhook on port 8080")
    await asyncio.Event().wait()  # бесконечное ожидание

if __name__ == '__main__':
    asyncio.run(main())