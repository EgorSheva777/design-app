import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiohttp import web

# Сюда вставь токен, который скопировал из BotFather
TOKEN = "8564511758:AAEZXs5ZGfRBBi29bUtv-QVD0rLZ5oPeRSU"
PORT = int(os.environ.get("PORT", 8080))

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Веб-заглушка для Render
async def handle(request):
    return web.Response(text="Бот работает!")

# Твой обработчик команд
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Бот успешно запущен на Render.")

async def main():
    # Запуск веб-сервера
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', PORT)
    await site.start()

    # Запуск бота
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
