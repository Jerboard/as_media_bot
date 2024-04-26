from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

from enums import UserButton


# кнопка для пользователя
def get_main_user_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=UserButton.MAIN.value, request_contact=True)]
        ],
        resize_keyboard=True
    )


def get_url_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='Вступить в Forbes Club', url=f'https://b24-hi5302.bitrix24.site')
    return kb.adjust(1).as_markup()


def get_send_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='Забрать фото', url=f'https://t.me/galaxystore_forbes30_bot')
    return kb.adjust(1).as_markup()
