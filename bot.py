import asyncio
import os
from aiogram import Bot, Dispatcher
from aiohttp import web

# Вставьте сюда ТОЛЬКО ЧТО полученный токен
TOKEN = "import asyncio
import os
from aiogram import Bot, Dispatcher
from aiohttp import web

# Вставьте сюда ТОЛЬКО ЧТО полученный токен
TOKEN = "8564511758:AAEyFFeixZql9tIRKj4Bv1w4ONiafJDHqrQ" 
PORT = int(os.environ.get("PORT", 8080))

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def handle(request):
    return web.Response(text="Бот работает")

async def main():
    # Запуск веб-сервера (необходим для Web Service на Render)
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', PORT)
    await site.start()

    # Очистка webhook для корректной работы через polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())" 
PORT = int(os.environ.get("PORT", 8080))

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def handle(request):
    return web.Response(text="Бот работает")

async def main():
    # Запуск веб-сервера (необходим для Web Service на Render)
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', PORT)
    await site.start()

    # Очистка webhook для корректной работы через polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
