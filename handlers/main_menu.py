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


# @dp.message()
# async def com_start(msg: Message, state: FSMContext):
#     print(msg.photo[-1].file_id)


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
    text = ('Спасибо, что поделились своим контактом! \n'
            'Мы отправим вам ссылку на фотоотчет с мероприятия, а пока расскажем немного о клубе  ⤵️ \n\n'
            '<b>Бизнес-сообщество Forbes Club</b> объединяет экспертных представителей разных отраслей экономики '
            'страны, оказывающих на нее непосредственное влияние.\n\n'
            'Резиденты клуба имеют возможность \n'
            '▫️ расширять контакты \n'
            '▫️ обмениваться опытом с ведущими игроками рынка\n'
            '▫️ посещать закрытые мероприятия\n'
            '▫️ заявлять о своих проектах на площадках Forbes\n\n'
            'Нажмите кнопку <u>«Вступить в клуб»</u> и узнайте подробности ⤵️')

    await msg.answer_photo(
        photo='AgACAgIAAxkBAANQZipljN7Y1hqOG6WRzTE9PPC2xJ0AAlnfMRt8FlFJ8pOp_ccc3vMBAAMCAAN5AAM0BA',
        caption=text,
        reply_markup=kb.get_url_kb()
    )

    await sleep(60)
    await sleep(60)
    await sleep(60)
    await sleep(60)
    await sleep(60)
    text = ('Первая часть фотографий уже доступна по ссылке \n\n'
            'Нажми ⤵️\n'
            'https://disk.yandex.ru/d/9ZlULYbRkUlHUw\n\n'
            'А чуть позже сегодня мы поделимся с вами и второй частью фотографий с мероприятия 🔜 \n\n'
            'Эти фото были сняты на Samsung Galaxy S24 Ultra во время вечера, они точно порадуют вас своим потрясным качеством!🔥 \n\n'
            'И на этом сюрпризы от партнера не заканчиваются…')
    await msg.answer(text)
    await sleep (60)
    await sleep (60)
    await sleep (60)
    await sleep (60)
    await sleep (60)
    text = ('Крутейшие фотки, снятые на флагманский смартфон уже готовы! 🤩\n'
            'Забирайте их и эксклюзивный подарок от фирменного магазина Samsung Galaxystore 🎁')
    await msg.answer(text=text, reply_markup=kb.get_send_kb())


# Отмена
@dp.callback_query(lambda cb: cb.data.startswith(BaseCB.CLOSE.value))
async def edit_start(cb: CallbackQuery, state: FSMContext):
    await cb.message.delete()
    await state.clear()
