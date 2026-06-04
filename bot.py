import os
import json
import logging
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, or_f
from aiogram.types import WebAppInfo, ReplyKeyboardMarkup, KeyboardButton
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

TOKEN = "8564511758:AAGCFWDIb1pURsyIwoDZRGoBxXnCbXSz0B4"
WEB_APP_URL = "https://egorsheva777.github.io/design-app/"

# ⚠️ ВСТАВЬ СЮДА СВОЙ ID ИЗ ТЕЛЕГРАМА ВМЕСТО ЭТИХ ЦИФР:
ADMIN_ID = 5995218415  

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
dp = Dispatcher()

TEXT_WELCOME = "Привет! Чтобы заказать дизайн, просто нажми на кнопку «Заказать дизайн 🚀» ниже 👇"

@dp.message(or_f(CommandStart(), F.text))
async def welcome_and_start(message: types.Message):
    logger.info(f"Запрос от {message.from_user.id}")
    kb = [[KeyboardButton(text="Заказать дизайн 🚀", web_app=WebAppInfo(url=WEB_APP_URL))]]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(TEXT_WELCOME, reply_markup=keyboard)

# ОБРАБОТКА ЗАЯВОК: Теперь отправляет лично тебе (ADMIN_ID)
@dp.message(F.web_app_data)
async def handle_webapp_data(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)
        user_info = f"👤 **Отправитель:** @{message.from_user.username or 'нет_юзернейма'} (ID: `{message.from_user.id}`)\n\n"
        
        if data.get("order_type") == "Дизайн":
            text = f"🎨 **Новый заказ!**\n\n" + user_info + f"Тариф: {data.get('tariff')}\nСроки: {data.get('deadline')}\n\nТЗ: {data.get('task')}"
        else:
            text = f"💼 **Бизнес-заявка!**\n\n" + user_info + f"Услуга: {data.get('tariff')}\nПроект: {data.get('project_info')}\n\nОписание: {data.get('task')}"
        
        # Отправляем уведомление администратору
        await bot.send_message(chat_id=ADMIN_ID, text=text)
        # А пользователю пишем, что всё ок
        await message.answer("Заявка принята! Скоро свяжемся. 👍")
        
    except Exception as e:
        logger.error(f"Ошибка обработки данных: {e}")
        try:
            await bot.send_message(chat_id=ADMIN_ID, text=f"⚠️ Ошибка получения заявки от {message.from_user.id}")
        except:
            pass
        await message.answer("Заявка принята! Скоро свяжемся. 👍")

async def handle_ping(request):
    return web.Response(text="Bot is alive and pulling!")

async def run_web_server():
    app = web.Application()
    app.router.add_get('/', handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()

async def main():
    await run_web_server()
    await bot.delete_webhook(drop_pending_updates=True)
    
    try:
        await bot.set_chat_menu_button(menu_button=types.MenuButtonDefault())
    except Exception as e:
        logger.error(f"Не удалось сбросить кнопку меню: {e}")
        
    logger.info("Бот запущен с пересылкой заявок админу!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
