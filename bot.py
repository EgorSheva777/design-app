import os
import json
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.types import WebAppInfo, ReplyKeyboardMarkup, KeyboardButton, Update
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(name)

TOKEN = os.environ.get("8564511758:AAGQGhRP-uSNtguy0aYXWTwP-7BWh9Arkrs")
if not TOKEN or TOKEN == "8564511758:AAGQGhRP-uSNtguy0aYXWTwP-7BWh9Arkrs":
TOKEN = "8564511758:AAGQGhRP-uSNtguy0aYXWTwP-7BWh9Arkrs" # Замените этот кусок на ваш реальный токен из BotFather!

WEB_APP_URL = "https://egorsheva777.github.io/design-app/"
RENDER_URL = os.environ.get("RENDER_EXTERNAL_URL")

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: types.Message):
logger.info(f"Старт от {message.from_user.id}")
kb = [[KeyboardButton(text="Заказать дизайн 🚀", web_app=WebAppInfo(url=WEB_APP_URL))]]
keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
await message.answer(f"Привет, {message.from_user.first_name}! 👋\nНажми на кнопку ниже.", reply_markup=keyboard)

@dp.message(F.web_app_data)
async def handle_webapp_data(message: types.Message):
try:
data = json.loads(message.web_app_data.data)
if data.get("order_type") == "Дизайн":
text = f"🎨 Новый заказ!\n\nТариф: {data.get('tariff')}\nСроки: {data.get('deadline')}\n\nТЗ: {data.get('task')}"
else:
text = f"💼 Бизнес-заявка!\n\nУслуга: {data.get('tariff')}\nПроект: {data.get('project_info')}\n\nОписание: {data.get('task')}"
await message.answer(text)
except Exception as e:
await message.answer("Заявка принята! Скоро свяжемся. 👍")

async def handle_webhook(request):
try:
body = await request.json()
update = Update.model_validate(body, context={"bot": bot})
await dp.feed_update(bot, update)
return web.Response(status=200)
except Exception as e:
return web.Response(status=500)

async def handle_ping(request):
return web.Response(text="Bot is alive!")

async def on_startup(app):
if RENDER_URL:
webhook_url = f"{RENDER_URL}/webhook"
logger.info(f"Ставим вебхук: {webhook_url}")
await bot.set_webhook(webhook_url, drop_pending_updates=True)

async def on_shutdown(app):
await bot.delete_webhook()

def main():
app = web.Application()
app.router.add_post('/webhook', handle_webhook)
app.router.add_get('/', handle_ping)
app.on_startup.append(on_startup)
app.on_cleanup.append(on_shutdown)
port = int(os.environ.get("PORT", 10000))
web.run_app(app, host='0.0.0.0', port=port)

if name == "main":
main()
