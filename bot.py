import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Ваш токен (или os.environ.get("TOKEN"))
TOKEN = "8564511758:AAEyFFeixZql9tIRKj4Bv1w4ONiafJDHqrQ"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я работаю! Вы успешно запустили бота в облаке.")

async def main():
    print("Бот успешно запущен!")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
