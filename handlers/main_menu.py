from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from aiogram.enums.content_type import ContentType

from asyncio import sleep

import db
import keyboards as kb
from init import dp, bot
from config import config
from utils.message_utils import send_message
from utils.entities_utils import recover_entities, save_entities
from enums import BaseCB


# команда старт
@dp.message(CommandStart())
async def com_start(msg: Message, state: FSMContext):
    if msg.from_user.id in config.admins:
        await msg.answer('<b>Меню:</b>', reply_markup=kb.get_main_admin_kb())

    else:
        await db.create_or_update_user(
            user_id=msg.from_user.id,
            full_name=msg.from_user.full_name,
            username=msg.from_user.username,
        )
        await send_message(chat_id=msg.from_user.id, wit_kb=True)


# команда старт
@dp.message(lambda msg: msg.content_type == ContentType.CONTACT)
async def take_contact(msg: Message):
    await db.update_user(user_id=msg.from_user.id, phone=msg.contact.phone_number)
    text = ('Спасибо, что поделились своим контактом! '
            'Завтра мы отправим вам ссылку на фотоотчет с мероприятия, а пока расскажем немного о клубе ⤵️\n\n\n'
            'Бизнес-сообщество Forbes Club объединяет экспертных представителей разных отраслей экономики страны, '
            'оказывающих на нее непосредственное влияние.\n\n'
            'Резиденты клуба имеют возможность расширять контакты и обмениваться опытом с ведущими игроками '
            'рынка, посещать закрытые мероприятия и заявлять о своих проектах на площадках Forbes.')

    await msg.answer_photo(
        photo='AgACAgIAAxkBAAM_Zipdk2lGEELXAyAFD8H3lnwamIUAAvHXMRsw8FFJUf8ToEemWhgBAAMCAAN5AAM0BA',
        caption=text,
        reply_markup=kb.get_url_kb()
    )


# Отмена
@dp.callback_query(lambda cb: cb.data.startswith(BaseCB.CLOSE.value))
async def edit_start(cb: CallbackQuery, state: FSMContext):
    await cb.message.delete()
    await state.clear()
