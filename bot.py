import asyncio
import os
from aiogram import Bot, Dispatcher
from aiohttp import web

# Настройки
TOKEN = "8564511758:AAEZXs5ZGfRBBi29bUtv-QVD0rLZ5oPeRSU"
PORT = int(os.environ.get("PORT", 8080))

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Простая заглушка для веб-сервера
async def handle(request):
    return web.Response(text="Бот работает!")

async def main():
    # Запуск веб-сервера (чтобы Render был доволен)
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', PORT)
    await site.start()

    print("Бот и веб-сервер запущены!")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
