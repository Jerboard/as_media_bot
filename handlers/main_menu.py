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
# @dp.message()
# async def com_start(msg: Message, state: FSMContext):
#     if msg.media_group_id:
#         await db.add_media_group_cache(
#             media_group_id=msg.media_group_id,
#             file_id=msg.photo[-1].file_id,
#             text=msg.caption,
#             entities=save_entities(msg.caption_entities))
#         media_in_cache = await db.get_all_media_group_cache(media_group_id=msg.media_group_id)
#         if len(media_in_cache) == 1:
#             await sleep(5)
#             photos = await db.get_all_media_group_cache (media_group_id=msg.media_group_id)
#             media_list = []
#             for photo in photos:
#                 media_list.append(
#                     InputMediaPhoto(
#                         media=photo.file_id,
#                         caption=photo.text,
#                         parse_mode=None,
#                         caption_entities=recover_entities(photo.entities)))
#
#             await bot.send_media_group(
#                 chat_id=msg.chat.id,
#                 media=media_list
#             )
#             await db.del_media_group_cache(media_group_id=msg.media_group_id)




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
async def take_contact(msg: Message, state: FSMContext):
    await db.update_user(user_id=msg.from_user.id, phone=msg.contact.phone_number)
    text = 'Пушка-бомба-ракета-торпеда! Ты лучший!!!'
    await msg.answer(text)


# Отмена
@dp.callback_query(lambda cb: cb.data.startswith(BaseCB.CLOSE.value))
async def edit_start(cb: CallbackQuery, state: FSMContext):
    await cb.message.delete()
    await state.clear()
