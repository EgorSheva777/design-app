import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv

# Загружаем данные из того самого секретного файла .env
load_dotenv()

TOKEN = os.getenv("TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    # Бот отвечает только вам, если ID совпадает
    if str(message.from_user.id) == str(ADMIN_ID):
        await message.answer("Привет, хозяин! Я успешно запущен через Secret Files!")
    else:
        await message.answer("Привет! Бот успешно работает в облаке.")

async def main():
    print("Бот успешно запущен!")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
