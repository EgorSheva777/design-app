import asyncio
import os
import json
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import WebAppInfo, ReplyKeyboardMarkup, KeyboardButton
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

# Настройка логирования
logging.basicConfig(level=logging.INFO)

TOKEN = "8564511758:AAH2DP__xRoNMOgJtMvnk8cMT5ABwXKOSz4"

# !!! ТВОЙ ID ИЗ @userinfobot (ЧИСЛО) !!!
# Твой ID администратора
ADMIN_ID = 5995218415  

bot = Bot(token=TOKEN)
@@ -22,8 +22,8 @@
# Обработчик команды /start
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    # УКАЖИ СВОЮ ССЫЛКУ НА MINI APP НИЖЕ
    mini_app_url = "https://egorsheva777.github.io/design-app/" 
    # Твоя ссылка на Mini App на Render
    mini_app_url = "https://egorsheva777.github.io/design-app/#" 

    reply_keyboard = ReplyKeyboardMarkup(
        keyboard=[[
@@ -76,28 +76,28 @@
async def index_handle(request):
    return web.Response(text="Bot is running smoothly!", content_type="text/plain")

# Функция, которая сработает строго в момент старта приложения
# Функция автоматической установки вебхука при старте
async def on_startup(bot: Bot):
    logging.info("Устанавливаем чистый вебхук...")
    await bot.set_webhook(
        url="https://design-app-test.onrender.com/webhook", # Твой актуальный вебхук URL
        drop_pending_updates=True # Сбрасываем зависшие старые апдейты, чтобы бот не тупил
        url="https://design-app-kohf.onrender.com/webhook", # ТОТ САМЫЙ АДРЕС, КОТОРЫЙ Я ИСПРАВИЛ
        drop_pending_updates=True 
    )

def main():
    app = web.Application()

    # Главная страница для cron-job.org
    # Главная страница для работы cron-job.org
    app.router.add_route('*', '/', index_handle)

    # Родной aiogram-обработчик вебхуков (автоматически закроет старые сессии)
    # Обработчик вебхуков aiogram
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot
    )
    webhook_requests_handler.register(app, path="/webhook")

    # Привязываем правильный startup/shutdown жизненный цикл
    # Связываем запуск приложения с установкой вебхука
    dp.startup.register(on_startup)
    setup_application(app, dp, bot=bot)
