from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_keybord() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text='Yes')
    keyboard.button(text='No')
    keyboard.adjust(2)
    return keyboard.as_markup(resize_keyboard=True)