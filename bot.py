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
from aiogram.webhook.aiohttp_impl import SimpleRequestHandler, setup_application

# Включаем логирование, чтобы детально видеть жизненный цикл бота на Render
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ==========================================
# КОНФИГУРАЦИЯ БОТА И СЕРВЕРА
# ==========================================
# Бот автоматически возьмет токен из настроек Environment Variables в Render
TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN or TOKEN == "8564511758:AAH2Ip789sQ5w_NzRhOKQWFrVIFk8mVsuXw":
    # Резервный токен (если переменные в панели Render не настроены)
    TOKEN = "8564511758:AAH2Ip789sQ5w_NzRhOKQWFrVIFk8mVsuXw" 

# Ссылка на ваше веб-приложение на GitHub Pages
WEB_APP_URL = "https://egorsheva777.github.io/design-app/"

# Render автоматически предоставляет эту переменную с вашим публичным адресом
RENDER_EXTERNAL_URL = os.environ.get("RENDER_EXTERNAL_URL")

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: types.Message):
    logger.info(f"Получена команда /start от пользователя {message.from_user.id}")
    
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

async def handle_ping(request):
    return web.Response(text="Бот и веб-сервер работают стабильно!")

async def on_startup(bot: Bot) -> None:
    if RENDER_EXTERNAL_URL:
        webhook_url = f"{RENDER_EXTERNAL_URL}/webhook"
        logger.info(f"[Webhook Mode] Регистрируем вебхук на URL: {webhook_url}")
        # drop_pending_updates=True мгновенно стирает все накопившиеся зависшие запросы
        await bot.set_webhook(webhook_url, drop_pending_updates=True)
    else:
        logger.info("[Polling Mode] Локальный запуск. Очищаем вебхуки...")
        await bot.delete_webhook(drop_pending_updates=True)

def main():
    # Регистрируем функцию, которая выполнится при старте бота
    dp.startup.register(on_startup)
    
    port = int(os.environ.get("PORT", 10000))

    if RENDER_EXTERNAL_URL:
        logger.info("[Render] Запуск сервера в режиме Webhook (без конфликтов портов и процессов)...")
        app = web.Application()
        app.router.add_get('/', handle_ping)

        # Настраиваем автоматический обработчик входящих сообщений от Telegram по пути /webhook
        webhook_requests_handler = SimpleRequestHandler(
            dispatcher=dp,
            bot=bot
        )
        webhook_requests_handler.register(app, path="/webhook")

        # Привязываем контекст aiogram к приложению aiohttp
        setup_application(app, dp, bot=bot)

        # Запускаем единый веб-сервер, который держит порт и принимает сообщения
        web.run_app(app, host='0.0.0.0', port=port)
    else:
        logger.info("[Local] Запуск в режиме Polling для локальной разработки...")
        async def run_polling():
            # Запускаем фоновый пинг-сервер, чтобы код вел себя идентично локально
            app = web.Application()
            app.router.add_get('/', handle_ping)
            runner = web.AppRunner(app)
            await runner.setup()
            site = web.TCPSite(runner, '0.0.0.0', port)
            await site.start()
            
            await bot.delete_webhook(drop_pending_updates=True)
            await dp.start_polling(bot)

        asyncio.run(run_polling())

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот остановлен пользователем")
