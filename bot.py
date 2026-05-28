import asyncio
import os
import json
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import WebAppInfo, ReplyKeyboardMarkup, KeyboardButton
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

# Настройка логирования
logging.basicConfig(level=logging.INFO)

TOKEN = "8564511758:AAH2DP__xRoNMOgJtMvnk8cMT5ABwXKOSz4"

# Твой ID администратора
ADMIN_ID = 5995218415  

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    # Твоя ссылка на Mini App на Render
    mini_app_url = "https://design-app-kohf.onrender.com" 
    
    reply_keyboard = ReplyKeyboardMarkup(
        keyboard=[[
            KeyboardButton(text="Заказать дизайн 🚀", web_app=WebAppInfo(url=mini_app_url))
        ]],
        resize_keyboard=True
    )
    
    await message.answer(
        "Привет! Нажми на кнопку ниже, чтобы открыть каталог и оформить заказ: 👇", 
        reply_markup=reply_keyboard
    )

# Обработчик данных из Mini App
@dp.message(F.web_app_data)
async def web_app_data_handler(message: types.Message):
    raw_data = message.web_app_data.data
    logging.info(f"=== ДАННЫЕ ПРИШЛИ: {raw_data} ===")
    
    text = f"🔔 <b>НОВАЯ ЗАЯВКА ИЗ MINI APP!</b>\n\n"
    text += f"👤 <b>Клиент:</b> {message.from_user.full_name}\n"
    if message.from_user.username:
        text += f"🔗 <b>Юзернейм:</b> @{message.from_user.username}\n"
    text += f"🆔 <b>ID клиента:</b> <code>{message.from_user.id}</code>\n"
    text += f"----------------------------------\n\n"
    
    try:
        order_info = json.loads(raw_data)
        if isinstance(order_info, dict):
            for key, value in order_info.items():
                text += f"🔹 <b>{key}:</b> {value}\n"
        else:
            text += f"📝 <b>Данные:</b> {order_info}"
    except Exception:
        text += f"📝 <b>Данные (строка):</b> {raw_data}"

    if ADMIN_ID != 0:
        try:
            await bot.send_message(chat_id=ADMIN_ID, text=text, parse_mode="HTML")
            logging.info("Заявка успешно переслана админу.")
        except Exception as admin_err:
            logging.error(f"Не удалось отправить сообщение админу: {admin_err}")

    try:
        await message.answer("Спасибо! Ваша заявка успешно отправлена администратору! ✅")
    except Exception as e:
        logging.error(f"Ошибка отправки ответа клиенту: {e}")

# Хендлер для пингатора (отвечает 200 OK на главную страницу)
async def index_handle(request):
    return web.Response(text="Bot is running smoothly!", content_type="text/plain")

# Функция автоматической установки вебхука при старте
async def on_startup(bot: Bot):
    logging.info("Устанавливаем чистый вебхук...")
    await bot.set_webhook(
        url="https://design-app-kohf.onrender.com/webhook", # ТОТ САМЫЙ АДРЕС, КОТОРЫЙ Я ИСПРАВИЛ
        drop_pending_updates=True 
    )

def main():
    app = web.Application()
    
    # Главная страница для работы cron-job.org
    app.router.add_route('*', '/', index_handle)
    
    # Обработчик вебхуков aiogram
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot
    )
    webhook_requests_handler.register(app, path="/webhook")
    
    # Связываем запуск приложения с установкой вебхука
    dp.startup.register(on_startup)
    setup_application(app, dp, bot=bot)
    
    port = int(os.environ.get('PORT', 10000))
    web.run_app(app, host='0.0.0.0', port=port)

if __name__ == "__main__":
    main()
