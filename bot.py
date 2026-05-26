import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiohttp import web

# СЮДА ВСТАВЬТЕ ТОЛЬКО ВАШ ТОКЕН ИЗ BOTFATHER
TOKEN = "8564511758:AAEZXs5ZGfRBBi29bUtv-QVD0rLZ5oPeRSU"

# Настройка порта для Render
PORT = int(os.environ.get("PORT", 8080))

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Заглушка для веб-сервера, чтобы Render не считал бота зависшим
async def handle(request):
    return web.Response(text="Бот активен")

# Обработка команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Бот успешно запущен и работает!")

async def main():
    # Запуск веб-сервера
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', PORT)
    await site.start()

    print("Сервис и бот запущены!")
    
    # Удаляем вебхук, чтобы polling работал корректно
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
