import asyncio
import os
from aiogram import Bot, Dispatcher
from aiohttp import web

# Вставьте сюда ВАШ НОВЫЙ ТОКЕН
TOKEN = "8564511758:AAEyFFeixZql9tIRKj4Bv1w4ONiafJDHqrQ"
PORT = int(os.environ.get("PORT", 8080))

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def handle(request):
    return web.Response(text="Бот работает")

async def main():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', PORT)
    await site.start()

    # Очистка старых обновлений, чтобы бот не "спотыкался"
    await bot.delete_webhook(drop_pending_updates=True)
    print("Бот успешно запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
