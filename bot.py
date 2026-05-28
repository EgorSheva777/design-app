import asyncio
import os
import json
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, ReplyKeyboardMarkup, KeyboardButton
from aiohttp import web

logging.basicConfig(level=logging.INFO)

TOKEN = "8564511758:AAH2DP__xRoNMOgJtMvnk8cMT5ABwXKOSz4"

# !!! СЮДА ВСТАВЬ СВОЙ РЕАЛЬНЫЙ ID ИЗ @userinfobot (Например: 512345678, без кавычек) !!!
# Если сомневаешься в ID, пока оставь 0, бот хотя бы не будет зависать у клиентов
ADMIN_ID = 5995218415  

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    # Укажи точную ссылку на свой Mini App (вместо примера ниже)
    mini_app_url = "https://egorsheva777.github.io/design-app/" 
    
    reply_keyboard = ReplyKeyboardMarkup(
        keyboard=[[
            KeyboardButton(text="Заказать дизайн 🚀", web_app=WebAppInfo(url=mini_app_url))
        ]],
        resize_keyboard=True
    )
    
    await message.answer(
        "Привет! Нажми на кнопку ниже, чтобы открыть каталог и оформить заказ: 👇", 
        reply_markup=reply_keyboard
    )

@dp.message(F.web_app_data)
async def web_app_data_handler(message: types.Message):
    raw_data = message.web_app_data.data
    logging.info(f"=== УРА, ДАННЫЕ ПРИШЛИ: {raw_data} ===")
    
    # Формируем текст для тебя
    text = f"🔔 **НОВАЯ ЗАЯВКА ИЗ MINI APP!**\n\n"
    text += f"👤 **Клиент:** {message.from_user.full_name}\n"
    if message.from_user.username:
        text += f"🔗 **Юзернейм:** @{message.from_user.username}\n"
    text += f"🆔 **ID клиента:** `{message.from_user.id}`\n"
    text += f"----------------------------------\n\n"
    
    try:
        order_info = json.loads(raw_data)
        if isinstance(order_info, dict):
            for key, value in order_info.items():
                text += f"🔹 **{key}:** {value}\n"
        else:
            text += f"📝 **Данные:** {order_info}"
    except Exception:
        text += f"📝 **Данные (строка):** {raw_data}"

    # БЕЗОПАСНАЯ ОТПРАВКА АДМИНИСТРАТОРУ
    if ADMIN_ID != 0:
        try:
            await bot.send_message(chat_id=ADMIN_ID, text=text)
            logging.info("Заявка успешно переслана админу в ЛС!")
        except Exception as admin_err:
            logging.error(f"Не удалось отправить сообщение админу на ID {ADMIN_ID}. Ошибка: {admin_err}")
            logging.error("Убедитесь, что ваш личный ID верный и вы запустили бота @userinfobot для проверки!")
    else:
        logging.warning("ADMIN_ID равен 0. Заявка никуда не отправлена, настройте ваш реальный Telegram ID!")

    # Этот ответ клиенту уйдет в любом случае, бот больше НЕ ЗАВИСНЕТ
    try:
        await message.answer("Спасибо! Ваша заявка успешно отправлена администратору! ✅")
    except Exception as e:
        logging.error(f"Ошибка отправки ответа клиенту: {e}")

async def index_handle(request):
    return web.Response(text="Bot is running smoothly!", content_type="text/plain")

async def tg_webhook_handle(request):
    try:
        body = await request.json()
        updater = types.Update.model_validate(body, context={"bot": bot})
        await dp.feed_update(bot, updater)
    except Exception as e:
        logging.error(f"Ошибка в вебхуке: {e}")
    return web.Response(text="OK")

async def on_startup(app):
    await bot.set_webhook(f"https://design-app-kohf.onrender.com/webhook")
    logging.info("Вебхук успешно инициализирован.")

async def on_shutdown(app):
    await bot.delete_webhook()

def main():
    app = web.Application()
    app.router.add_route('*', '/', index_handle)
    app.router.add_post('/webhook', tg_webhook_handle)
    
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    
    port = int(os.environ.get('PORT', 10000))
    web.run_app(app, host='0.0.0.0', port=port)

if __name__ == "__main__":
    main()
