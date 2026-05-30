import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

class SimpleHTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Отправляем успешный статус 200 ОК, чтобы Render видел, что приложение "живо"
        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write("Бот успешно запущен и работает!".encode("utf-8"))

    def log_message(self, format, *args):
        # Отключаем лишний спам логов веб-сервера в консоль Render
        return

def run_health_check_server():
    # Render автоматически передает нужный порт в переменную окружения PORT
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), SimpleHTTPHandler)
    print(f"[Render Fix] Фоновый веб-сервер успешно запущен на порту {port}")
    server.serve_forever()

# Запускаем сервер в отдельном потоке (thread), чтобы он не блокировал работу самого Телеграм-бота
threading.Thread(target=run_health_check_server, daemon=True).start()

# =====================================================================
# ДАЛЕЕ ВАШ СУЩЕСТВУЮЩИЙ КОД БОТА (например, import telebot, bot.infinity_polling() и т.д.)
# =====================================================================
import os
import json
import asyncio
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.types import WebAppInfo, ReplyKeyboardMarkup, KeyboardButton

# 1. ВСТАВЬ СВОЙ ТОКЕН СЮДА (от @BotFather)
TOKEN = "8564511758:AAH2Ip789sQ5w_NzRhOKQWFrVIFk8mVsuXw"

# 2. ВСТАВЬ ССЫЛКУ НА ТВОЙ САЙТ GITHUB PAGES СЮДА
# Ссылка должна выглядеть так: https://твой_логин.github.io/название_репозитория/
WEB_APP_URL = "https://egorsheva777.github.io/design-app/"

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
