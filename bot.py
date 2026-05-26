import asyncio
from aiogram import Bot, Dispatcher

# Вставь сюда свой токен от BotFather
TOKEN = "8564511758:AAEZXs5ZGfRBBi29bUtv-QVD0rLZ5oPeRSU"

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    print("Бот запущен!")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
