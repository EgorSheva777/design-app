import asyncio
import os
from aiogram import Bot, Dispatcher
from aiohttp import web

# Твой токен
TOKEN = "8564511758:AAEZxs5ZGfRBBi29bUtV-QVD0rLZ5oPeRSU"
# Порт, который дает Render
PORT = int(os.environ.get("PORT", 8080))

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Заглушка для веб-сервера (Render требует, чтобы мы отвечали на запросы)
async def handle(request):
    return web.Response(text="Бот работает!")

async def main():
    # Запуск веб-сервера
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', PORT)
    await site.start()

    print("Бот и веб-сервер запущены!")
    
    # Запуск бота
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
