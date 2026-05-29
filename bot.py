import os
import json
import asyncio
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.types import WebAppInfo, ReplyKeyboardMarkup, KeyboardButton

# 1. ВСТАВЬ СВОЙ ТОКЕН СЮДА (от @BotFather)
TOKEN = "ТВОЙ_ТОКЕН_БОТА"

# 2. ВСТАВЬ ССЫЛКУ НА ТВОЙ САЙТ GITHUB PAGES СЮДА
# Ссылка должна выглядеть так: https://твой_логин.github.io/название_репозитория/
WEB_APP_URL = "https://твой_логин.github.io/название_репозитория/"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: types.Message):
    # Создаем кнопку, которая открывает Mini App
    kb = [
        [KeyboardButton(text="🎨 Заказать дизайн", web_app=WebAppInfo(url=WEB_APP_URL))]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    
    await message.answer(
        f"Привет, {message.from_user.first_name}! 👋\nНажми на кнопку ниже, чтобы открыть приложение.",
        reply_markup=keyboard
    )

@dp.message(F.web_app_data)
async def handle_webapp_data(message: types.Message):
    """Этот блок сработает, когда ты нажмешь 'Отправить заказ' в HTML"""
    try:
        # Получаем данные из Mini App
        data = json.loads(message.web_app_data.data)
        
        tariff = data.get("tariff", "Не выбран")
        deadline = data.get("deadline", "Не указан")
        task = data.get("task", "Нет описания")

        text = (
            "🚀 **Получен новый заказ!**\n\n"
            f"👤 **От:** {message.from_user.full_name}\n"
            f"💎 **Тариф:** {tariff}\n"
            f"⏳ **Срок:** {deadline}\n"
            f"📝 **Задание:** {task}"
        )
        
        await message.answer(text, parse_mode="Markdown")
        
    except Exception as e:
        await message.answer(f"Ошибка при получении данных: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
