from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardBuilder

from enums import AdminCB, group_user


# Главная клавиатура админов
def get_main_admin_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='📝 Изменить картинку', callback_data=f'{AdminCB.EDIT.value}:photo')
    kb.button(text='📝 Изменить текст', callback_data=f'{AdminCB.EDIT.value}:text')
    kb.button(text='✉️ Отправить сообщение', callback_data=AdminCB.SEND_START.value)
    kb.button(text='🗂 Данные пользователей', callback_data=AdminCB.DOCUMENT.value)
    return kb.adjust(1).as_markup()


# Главная клавиатура админов
def get_send_group_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for k, v in group_user.items():
        kb.button(text=v, callback_data=f'{AdminCB.WAIT.value}:{k}')
    kb.button(text='🔙 Назад', callback_data=AdminCB.BACK.value)
    return kb.adjust(1).as_markup()


def get_cancel_admin_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='❌ Отмена', callback_data=f'{AdminCB.BACK.value}')
    return kb.adjust(1).as_markup()