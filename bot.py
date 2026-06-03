import os
import json
import logging
import asyncio
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.types import WebAppInfo, ReplyKeyboardMarkup, KeyboardButton
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# ТВОЙ ТОКЕН И ССЫЛКИ
TOKEN = "8564511758:AAGCFWDIb1pURsyIwoDZRGoBxXnCbXSz0B4"
WEB_APP_URL = "https://egorsheva777.github.io/design-app/"

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
dp = Dispatcher()

TEXT_WELCOME = "Привет! Чтобы заказать дизайн, просто нажми на кнопку «Заказать дизайн 🚀» ниже 👇"

# 1. ХЕНДЛЕР НА ЛЮБОЕ СООБЩЕНИЕ ИЛИ СТАРТ (Показывает кнопку)
@dp.message(or_f(CommandStart(), F.text))
async def welcome_and_start(message: types.Message):
    logger.info(f"Запрос от {message.from_user.id}")
    
    kb = [[KeyboardButton(text="Заказать дизайн 🚀", web_app=WebAppInfo(url=WEB_APP_URL))]]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    
    await message.answer(TEXT_WELCOME, reply_markup=keyboard)

# 2. ОБРАБОТКА ДАННЫХ ИЗ МИНИ-АПП (Твоя логика заказов полностью сохранена!)
@dp.message(F.web_app_data)
async def handle_webapp_data(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)
        if data.get("order_type") == "Дизайн":
            text = f"🎨 **Новый заказ!**\n\nТариф: {data.get('tariff')}\nСроки: {data.get('deadline')}\n\nТЗ: {data.get('task')}"
        else:
            text = f"💼 **Бизнес-заявка!**\n\nУслуга: {data.get('tariff')}\nПроект: {data.get('project_info')}\n\nОписание: {data.get('task')}"
        await message.answer(text)
    except Exception as e:
        logger.error(f"Ошибка обработки данных: {e}")
        await message.answer("Заявка принята! Скоро свяжемся. 👍")

# Используем вспомогательную функцию для фильтра или импортируем ее
from aiogram.filters import or_f

# 3. ГЛАВНЫЙ ЗАПУСК ЧЕРЕЗ POLLING (БЕЗ ПОРТОВ)
async def main():
    print("Бот успешно переведен на Long Polling! На Render ничего не упадет.")
    
    # Сбрасываем старые вебхуки, которые вешали сервер
    await bot.delete_webhook(drop_pending_updates=True)
    
    # Меняем кнопку "Меню" в углу ТГ, чтобы она ВСЕГДА открывала твой дизайн-апп
    await bot.set_chat_menu_button(
        menu_button=types.MenuButtonWebApp(text="Заказать дизайн 🎨", web_app=WebAppInfo(url=WEB_APP_URL))
    )
    
    # Запускаем бесконечный опрос
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
