from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from enums import UserButton


# кнопка для пользователя
def get_main_user_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=UserButton.MAIN.value, request_contact=True)
            ]
        ],
        resize_keyboard=True
    )
