import os
import json
import asyncio
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.types import WebAppInfo, ReplyKeyboardMarkup, KeyboardButton
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# Включаем логирование, чтобы видеть действия бота в консоли Render
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ==========================================
# КОНФИГУРАЦИЯ БОТА
# ==========================================
# Бот попробует взять токен из переменных окружения (Environment Variables) в Render.
# Если вы их не настраивали, укажите ваш токен вместо заглушки ниже.
TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN or TOKEN == "8564511758:AAH2Ip789sQ5w_NzRhOKQWFrVIFk8mVsuXw":
    # ВСТАВЬТЕ ВАШ ТОКЕН СЮДА, ЕСЛИ НЕ ИСПОЛЬЗУЕТЕ ПЕРЕМЕННЫЕ ОКРУЖЕНИЯ RENDER:
    TOKEN = "8564511758:AAH2Ip789sQ5w_NzRhOKQWFrVIFk8mVsuXw" 

# Ссылка на ваш сайт на GitHub Pages
WEB_APP_URL = "https://egorsheva777.github.io/design-app/"

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: types.Message):
    logger.info(f"Получена команда /start от пользователя {message.from_user.id}")
    
    # Кнопка для открытия веб-приложения Mini App
    kb = [
        [KeyboardButton(text="Заказать дизайн 🚀", web_app=WebAppInfo(url=WEB_APP_URL))]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    
    await message.answer(
        f"Привет, {message.from_user.first_name}! 👋\nНажми на кнопку ниже, чтобы открыть приложение.",
        reply_markup=keyboard
    )

@dp.message(F.web_app_data)
async def handle_webapp_data(message: types.Message):
    logger.info(f"Получены данные от Mini App для пользователя {message.from_user.id}")
    try:
        data = json.loads(message.web_app_data.data)
        
        if data.get("order_type") == "Дизайн":
            text = (
                f"🎨 **Получен новый заказ на дизайн!**\n\n"
                f"Тариф: `{data.get('tariff')}`\n"
                f"Сроки: `{data.get('deadline')}`\n\n"
                f"📝 **ТЗ:** {data.get('task')}"
            )
        else:
            text = (
                f"💼 **Получена заявка на бизнес-услугу!**\n\n"
                f"Услуга: `{data.get('tariff')}`\n"
                f"Проект: `{data.get('project_info')}`\n\n"
                f"📝 **Описание:** {data.get('task')}"
            )
            
        await message.answer(text)
    except Exception as e:
        logger.error(f"Ошибка парсинга данных Mini App: {e}")
        await message.answer(f"Заявка успешно принята! Наш менеджер свяжется с вами в ближайшее время. 👍")

# ==========================================
# ВЕБ-СЕРВЕР ДЛЯ ОБХОДА ПРОВЕРОК ПОРТОВ RENDER
# ==========================================
runner = None
site = None

async def handle_ping(request):
    return web.Response(text="Бот работает стабильно!")

async def start_background_server():
    global runner, site
    app = web.Application()
    app.router.add_get('/', handle_ping)
    
    # Порт 10000 используется по умолчанию на бесплатном тарифе Render
    port = int(os.environ.get("PORT", 10000))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    logger.info(f"[Render Fix] Асинхронный веб-сервер успешно запущен на порту {port}")

# Главная точка входа в программу
async def main():
    # Запускаем фоновый сервер для пинга со стороны Render
    await start_background_server()
    
    # Принудительно очищаем очередь обновлений и сбрасываем старые вебхуки
    logger.info("Сброс вебхуков и очистка зависших сообщений Telegram...")
    await bot.delete_webhook(drop_pending_updates=True)
    
    # Запускаем прослушивание сообщений бота
    logger.info("Запуск поллинга...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот остановлен пользователем")
