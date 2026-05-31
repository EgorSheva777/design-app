import os
import json
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.types import WebAppInfo, ReplyKeyboardMarkup, KeyboardButton

# ==========================================
# 1. ВСТАВЬ СВОЙ РЕАЛЬНЫЙ ТОКЕН СЮДА (от @BotFather)
TOKEN = "8564511758:AAH2Ip789sQ5w_NzRhOKQWFrVIFk8mVsuXw"

# 2. ССЫЛКА НА ТВОЙ САЙТ GITHUB PAGES СЮДА
WEB_APP_URL = "https://egorsheva777.github.io/design-app/"
# ==========================================

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: types.Message):
    # Создаем кнопку, которая открывает Mini App
    kb = [
        [KeyboardButton(text="Заказать дизайн 🚀", web_app=WebAppInfo(url=WEB_APP_URL))]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    
    await message.answer(
        f"Привет, {message.from_user.first_name}! 👋\nНажми на кнопку ниже, чтобы открыть приложение.",
        reply_markup=keyboard
    )

@dp.message(F.web_app_data)
async def handle_webapp_data(message: types.Message):
    # Обработка данных, пришедших из Mini App
    try:
        data = json.loads(message.web_app_data.data)
        
        if data.get("order_type") == "Дизайн":
            text = (
                f"🎨 **Получен новый заказ на дизайн!**\n\n"
                f"Тариф: `{data.get('tariff')}`\n"
                f"Сроки: `{data.get('deadline')}`\n\n"
                f"📝 **ТЗ:** {data.get('task')}"
            )
        else:
            text = (
                f"💼 **Получена заявка на бизнес-услугу!**\n\n"
                f"Услуга: `{data.get('tariff')}`\n"
                f"Проект: `{data.get('project_info')}`\n\n"
                f"📝 **Описание:** {data.get('task')}"
            )
            
        await message.answer(text, parse_mode="Markdown")
    except Exception as e:
        await message.answer(f"Заявка принята! Скоро наш менеджер свяжется с вами для уточнения деталей. 👍")

# ==========================================
# ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ ДЛЯ ЗАЩИТЫ ОТ СБОРЩИКА МУСОРА RENDER
# ==========================================
runner = None
site = None

async def handle_ping(request):
    return web.Response(text="Bot is alive!")

async def start_background_server():
    global runner, site
    app = web.Application()
    app.router.add_get('/', handle_ping)
    
    # Render передает порт в переменной окружения PORT, по умолчанию берем 10000
    port = int(os.environ.get("PORT", 10000))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"[Render Fix] Асинхронный веб-сервер успешно запущен на порту {port}", flush=True)

# Главная точка входа
async def main():
    # Запускаем фоновый веб-сервер
    await start_background_server()
    
    # СБРОС И ОЧИСТКА КОНФЛИКТОВ (Удаляет старые вебхуки и очищает очередь сообщений)
    print("Принудительно очищаем очередь сообщений и сбрасываем вебхуки...", flush=True)
    await bot.delete_webhook(drop_pending_updates=True)
    
    # Запускаем поллинг бота Телеграм
    print("Бот успешно запущен и готов принимать сообщения...", flush=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
