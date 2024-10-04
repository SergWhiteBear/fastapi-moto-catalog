import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import WebAppInfo
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio
from config import BOT_TOKEN

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Логирование
logging.basicConfig(level=logging.INFO)


# Обработчик команды /start
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Каталог мотоциклов", web_app=WebAppInfo(url="https://d2ce-109-195-105-142.ngrok-free.app"))
    await message.answer(
        "Добро пожаловать в магазин мотоциклов! Откройте наш каталог, чтобы выбрать мотоцикл:",
        reply_markup=keyboard.as_markup()
    )


async def main():
    # Запуск диспетчера
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
