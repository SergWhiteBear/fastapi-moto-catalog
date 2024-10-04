from aiogram.filters import Command
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove

from src.bot.keybords.simple_keybord import get_keybord

router = Router()

@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "Hello, my little friend! Can I help you?",
        reply_markup=get_keybord()
    )

@router.message(F.text.lower() == 'yes')
async def yes_handler(message: Message):
    await message.answer(
        "How I can help you?",
        reply_markup=ReplyKeyboardRemove(),
    )

@router.message(F.text.lower() == 'no')
async def no_handler(message: Message):
    await message.answer(
        "Ok! Bye, bye! :)",
        reply_markup=ReplyKeyboardRemove()
    )