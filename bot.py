import asyncio
import os
import json
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiohttp import web

# Включаем логирование
logging.basicConfig(level=logging.INFO)

TOKEN = "8564511758:AAH2DP__xRoNMOgJtMvnk8cMT5ABwXKOSz4"
ADMIN_ID = 5995218415  
RENDER_URL = "https://design-app-kohf.onrender.com"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    # Вставь сюда свою ссылку на Mini App
    mini_app_url = "https://egorsheva777.github.io/design-app/" 
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text="Открыть Mini App 🚀", web_app=WebAppInfo(url=mini_app_url))
        ]]
    )
    await message.answer("Привет! Нажми на кнопку ниже, чтобы оформить заказ: 👇", reply_markup=keyboard)

# Обработка данных из Mini App
@dp.message(F.web_app_data)
async def web_app_data_handler(message: types.Message):
    logging.info(f"=== ДАННЫЕ ПОЛУЧЕНЫ: {message.web_app_data.data} ===")
    raw_data = message.web_app_data.data
    text = "🔔 **Новая заявка из Mini App!**\n\n"
    
    try:
        order_info = json.loads(raw_data)
        if isinstance(order_info, dict):
            for key, value in order_info.items():
                text += f"🔹 **{key}:** {value}\n"
        else:
            text += f"📝 **Данные:** {order_info}"
    except Exception:
        text += f"📝 **Данные заказа:** {raw_data}"

    await bot.send_message(chat_id=ADMIN_ID, text=text)
    await message.answer("Спасибо! Твоя заявка успешно отправлена! ✅")

# ОТВЕТ ДЛЯ RENDER (Убирает ошибку 404 на главной)
async def index_handle(request):
    return web.Response(text="Bot is perfectly running!", content_type="text/plain")

# Прием вебхуков от Telegram
async def tg_webhook_handle(request):
    try:
        body = await request.json()
        updater = types.Update.model_validate(body, context={"bot": bot})
        await dp.feed_update(bot, updater)
    except Exception as e:
        logging.error(f"Ошибка внутри вебхука: {e}")
    return web.Response(text="OK")

async def on_startup(app):
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(f"{RENDER_URL}/webhook", drop_pending_updates=True)
    logging.info("Вебхук успешно установлен!")

async def on_shutdown(app):
    await bot.delete_webhook()

def main():
    app = web.Application()
    # Теперь Render будет стучаться сюда и получать 200 OK
    app.router.add_get('/', index_handle)
    app.router.add_post('/webhook', tg_webhook_handle)
    
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    
    port = int(os.environ.get('PORT', 10000))
    web.run_app(app, host='0.0.0.0', port=port)

if __name__ == "__main__":
    main()
