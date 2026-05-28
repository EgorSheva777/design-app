import asyncio
import os
import json
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, ReplyKeyboardMarkup, KeyboardButton
from aiohttp import web

# Логирование
logging.basicConfig(level=logging.INFO)

TOKEN = "8564511758:AAH2DP__xRoNMOgJtMvnk8cMT5ABwXKOSz4"
ADMIN_ID = 5995218415  
RENDER_URL = "https://design-app-kohf.onrender.com"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    # !!! ТВОЯ ССЫЛКА НА MINI APP !!!
    mini_app_url = "https://egorsheva777.github.io/design-app/" 
    
    # 1. Кнопка под сообщением (Inline)
    inline_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text="Открыть Mini App 🚀", web_app=WebAppInfo(url=mini_app_url))
        ]]
    )
    
    # 2. Нижняя текстовая кнопка (ОБЯЗАТЕЛЬНО для работы простого message.web_app_data)
    # Через неё данные гарантированно прилетят в бота при закрытии
    reply_keyboard = ReplyKeyboardMarkup(
        keyboard=[[
            KeyboardButton(text="Заказать дизайн 🚀", web_app=WebAppInfo(url=mini_app_url))
        ]],
        resize_keyboard=True
    )
    
    await message.answer(
        "Привет! У нас появилось приложение MiniApp. Нажми на кнопку ниже, чтобы открыть и оформить заказ: 👇", 
        reply_markup=reply_keyboard # Показываем нижнюю кнопку по умолчанию
    )

# ОБРАБОТЧИК ДАННЫХ ИЗ MINI APP
@dp.message(F.web_app_data)
async def web_app_data_handler(message: types.Message):
    logging.info(f"=== УРА, ДАННЫЕ ПРИШЛИ: {message.web_app_data.data} ===")
    raw_data = message.web_app_data.data
    text = "🔔 **Новая заявка из Mini App!**\n\n"
    
    try:
        order_info = json.loads(raw_data)
        if isinstance(order_info, dict):
            for key, value in order_info.items():
                text += f"🔹 **{key}:** {value}\n"
        else:
            text += f"📝 **Данные заказа:** {order_info}"
    except Exception:
        text += f"📝 **Данные заказа (строка):** {raw_data}"

    # Отправка администратору
    await bot.send_message(chat_id=ADMIN_ID, text=text)
    # Ответ пользователю
    await message.answer("Спасибо! Твоя заявка успешно получена и отправлена администратору! ✅")

# Ответ для Render (GET/HEAD)
async def index_handle(request):
    return web.Response(text="Bot is running smoothly!", content_type="text/plain")

# Прием вебхуков
async def tg_webhook_handle(request):
    try:
        body = await request.json()
        updater = types.Update.model_validate(body, context={"bot": bot})
        await dp.feed_update(bot, updater)
    except Exception as e:
        logging.error(f"Ошибка в вебхуке: {e}")
    return web.Response(text="OK")

async def on_startup(app):
    # ВНИМАНИЕ: убрали drop_pending_updates=True, теперь сообщения не сгорают!
    await bot.set_webhook(f"{RENDER_URL}/webhook")
    logging.info("Вебхук успешно инициализирован.")

async def on_shutdown(app):
    await bot.delete_webhook()

def main():
    app = web.Application()
    app.router.add_route('*', '/', index_handle)
    app.router.add_post('/webhook', tg_webhook_handle)
    
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    
    port = int(os.environ.get('PORT', 10000))
    web.run_app(app, host='0.0.0.0', port=port)

if __name__ == "__main__":
    main()
