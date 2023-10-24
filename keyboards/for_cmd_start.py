from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


def get_show_create_kb():
    buttons = [
        [
            types.InlineKeyboardButton(
                text="Create new task", callback_data="a_createTask"
            ),
            types.InlineKeyboardButton(
                text="Show my tasks", callback_data="a_showTaskList"
            ),
        ],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
