import os
import json
import logging
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, or_f
from aiogram.types import WebAppInfo, ReplyKeyboardMarkup, KeyboardButton
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

TOKEN = "8564511758:AAGCFWDIb1pURsyIwoDZRGoBxXnCbXSz0B4"
WEB_APP_URL = "https://egorsheva777.github.io/design-app/"

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
dp = Dispatcher()

TEXT_WELCOME = "Привет! Чтобы заказать дизайн, просто нажми на кнопку «Заказать дизайн 🚀» ниже 👇"

@dp.message(or_f(CommandStart(), F.text))
async def welcome_and_start(message: types.Message):
    logger.info(f"Запрос от {message.from_user.id}")
    kb = [[KeyboardButton(text="Заказать дизайн 🚀", web_app=WebAppInfo(url=WEB_APP_URL))]]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(TEXT_WELCOME, reply_markup=keyboard)

@dp.message(F.web_app_data)
async def handle_webapp_data(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)
        if data.get("order_type") == "Дизайн":
            text = f"🎨 **Новый заказ!**\n\nТариф: {data.get('tariff')}\nСроки: {data.get('deadline')}\n\nТЗ: {data.get('task')}"
        else:
            text = f"💼 **Бизнес-заявка!**\n\nУслуга: {data.get('tariff')}\nПроект: {data.get('project_info')}\n\nОписание: {data.get('task')}"
        await message.answer(text)
    except Exception as e:
        logger.error(f"Ошибка обработки данных: {e}")
        await message.answer("Заявка принята! Скоро свяжемся. 👍")

# Заглушка для Render, чтобы он не ругался на порты и думал, что это сайт
async def handle_ping(request):
    return web.Response(text="Bot is alive and pulling!")

async def run_web_server():
    app = web.Application()
    app.router.add_get('/', handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    logger.info(f"Микро-сервер для обмана Render запущен на порту {port}")

async def main():
    # Запускаем фоновый веб-сервер для бесплатного тарифа Render
    await run_web_server()
    
    # Сносим старые вебхуки, переходим на пуллинг
    await bot.delete_webhook(drop_pending_updates=True)
    
    # Ставим кнопку меню
    try:
        await bot.set_chat_menu_button(
            menu_button=types.MenuButtonWebApp(text="Заказать дизайн 🎨", web_app=WebAppInfo(url=WEB_APP_URL))
        )
    except Exception as e:
        logger.error(f"Не удалось поставить кнопку меню: {e}")
        
    logger.info("Бот успешно запущен в режиме Long Polling!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
