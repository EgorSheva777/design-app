import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv

# Метод подгружает токен и ID из твоего созданного Secret File (.env)
load_dotenv()

TOKEN = os.getenv("TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    # Проверка: если пишет создатель, бот отвечает по-особенному
    if str(message.from_user.id) == str(ADMIN_ID):
        await message.answer("Бот успешно запущен! Приветствую, админ!")
    else:
        await message.answer("Привет! Бот работает в штатном режиме.")

async def main():
    # Чистим старые вебхуки, чтобы убрать конфликты
    await bot.delete_webhook(drop_pending_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
