from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.enums.content_type import ContentType
from aiogram.filters import StateFilter
from asyncio import sleep

import os

import db
import keyboards as kb
from init import dp, bot
from config import config
from utils.entities_utils import save_entities, recover_entities
from utils.message_utils import send_message
from enums import AdminCB, AdminStatus, group_user


# Изменить запись
@dp.callback_query(lambda cb: cb.data.startswith(AdminCB.EDIT.value))
async def edit_start(cb: CallbackQuery, state: FSMContext):
    _, action = cb.data.split(':')

    await state.set_state (AdminStatus.EDIT)
    await state.update_data (action=action)
    if action == 'photo':
        await cb.message.answer('Отправьте новую картинку', reply_markup=kb.get_cancel_admin_kb())
    else:
        await cb.message.answer('Отправьте новый текст', reply_markup=kb.get_cancel_admin_kb())


# принимает изменения
@dp.message(StateFilter(AdminStatus.EDIT))
async def edit_message(msg: Message, state: FSMContext):
    data = await state.get_data()
    action = data.get('action')
    await state.clear()

    if action == 'photo':
        await db.update_info(photo_id=msg.photo[-1].file_id)
        await msg.answer('✅ Картинка обновлена')
    else:
        entities = save_entities(msg.entities)
        await db.update_info(text=msg.text, entities=entities)
        await msg.answer('✅ Текст обновлен')

    await send_message(msg.chat.id)
    await msg.answer ('<b>Меню:</b>', reply_markup=kb.get_main_admin_kb ())


# Изменить запись
@dp.callback_query(lambda cb: cb.data.startswith(AdminCB.SEND_START.value))
async def send_start(cb: CallbackQuery, state: FSMContext):
    text = 'Выберите группу пользователей'
    await cb.message.edit_text(text, reply_markup=kb.get_send_group_kb())


# ожидаем сообщения
@dp.callback_query(lambda cb: cb.data.startswith(AdminCB.WAIT.value))
async def send_start(cb: CallbackQuery, state: FSMContext):
    _, group = cb.data.split(':')

    group_str = group_user[group]
    text = f'Отправьте сообщение сообщение получит группа "{group_str}"'
    await state.set_state(AdminStatus.SEND)
    await state.update_data(group=group)
    await cb.message.edit_text(text, reply_markup=kb.get_cancel_admin_kb())


# принимает изменения
@dp.message(StateFilter(AdminStatus.SEND))
async def edit_message(msg: Message, state: FSMContext):
    # sent = await msg.answer('⏳')

    data = await state.get_data()
    await state.clear()
    group = data.get('group')
    with_phone = True if group == 'with_phone' else False
    users = await db.get_users(with_phone=with_phone)

    counter = 0

    if msg.media_group_id:
        await db.add_media_group_cache (
            media_group_id=msg.media_group_id,
            file_id=msg.photo [-1].file_id,
            text=msg.caption,
            entities=save_entities (msg.caption_entities)
        )
        media_in_cache = await db.get_all_media_group_cache (media_group_id=msg.media_group_id)
        if len (media_in_cache) > 1:
            return

        else:
            sent = await msg.answer ('⏳')
            await sleep (config.wait_media_group)
            photos = await db.get_all_media_group_cache (media_group_id=msg.media_group_id)
            media_list = []
            for photo in photos:
                media_list.append (
                    InputMediaPhoto (
                        media=photo.file_id,
                        caption=photo.text,
                        parse_mode=None,
                        caption_entities=recover_entities (photo.entities)))

            for user in users:
                try:
                    await bot.send_media_group (
                        chat_id=user.user_id,
                        media=media_list
                    )
                    counter += 1
                except Exception as ex:
                    print(ex)
                    pass
            await db.del_media_group_cache (media_group_id=msg.media_group_id)

    else:
        sent = await msg.answer ('⏳')
        for user in users:
            try:
                if msg.content_type == ContentType.TEXT:
                    await bot.send_message(chat_id=user.user_id, text=msg.text, entities=msg.entities, parse_mode=None)

                elif msg.content_type == ContentType.PHOTO:
                    await bot.send_photo(
                        chat_id=user.user_id,
                        photo=msg.photo[-1].file_id,
                        caption=msg.caption,
                        caption_entities=msg.caption_entities,
                        parse_mode=None
                    )

                elif msg.content_type == ContentType.VIDEO:
                    await bot.send_video (
                        chat_id=user.user_id,
                        video=msg.video.file_id,
                        caption=msg.caption,
                        caption_entities=msg.caption_entities,
                        parse_mode=None
                    )

                elif msg.content_type == ContentType.VIDEO_NOTE:
                    await bot.send_video_note (
                        chat_id=user.user_id,
                        video_note=msg.video_note.file_id,
                    )

                elif msg.content_type == ContentType.VOICE:
                    await bot.send_voice (
                        chat_id=user.user_id,
                        voice=msg.voice.file_id,
                    )

                elif msg.content_type == ContentType.ANIMATION:
                    await bot.send_animation (
                        chat_id=user.user_id,
                        animation=msg.animation.file_id,
                        caption=msg.caption,
                        caption_entities=msg.caption_entities,
                        parse_mode=None
                    )

                elif msg.content_type == ContentType.DOCUMENT:
                    await bot.send_document (
                        chat_id=user.user_id,
                        document=msg.document.file_id,
                        caption=msg.caption,
                        caption_entities=msg.caption_entities,
                        parse_mode=None
                    )

                else:
                    await msg.answer('❌ Ни одно сообщение не отправлено. Неподдерживаемый формат сообщения')
                    break

                counter += 1
            except Exception as ex:
                print(ex)
                pass

    await sent.edit_text(f'✅ Сообщение отправлено {counter} пользователям')
    await msg.answer ('<b>Меню:</b>', reply_markup=kb.get_main_admin_kb ())


# отправить список пользователей в csv
@dp.callback_query(lambda cb: cb.data.startswith(AdminCB.DOCUMENT.value))
async def back_start(cb: CallbackQuery, state: FSMContext):
    users = await db.get_users (all_users=True)
    if not os.path.exists(config.path):
        os.makedirs(config.path)

    file_path = os.path.join (config.path, 'users.csv')
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write('ID;Создан;Обновлён;Полное имя;Имя пользователя;Телефон;\n')
        for user in users:
            file.write(f'{user.user_id};{user.created_at};{user.updated_at};{user.full_name};{user.username};{user.phone};\n')

    user_db_file = FSInputFile(file_path)
    await cb.message.answer_document(document=user_db_file)
    os.remove(file_path)
    await cb.message.answer('<b>Меню:</b>', reply_markup=kb.get_main_admin_kb())


# вернуть главный экран
@dp.callback_query(lambda cb: cb.data.startswith(AdminCB.BACK.value))
async def back_start(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    await cb.message.edit_text('<b>Меню:</b>', reply_markup=kb.get_main_admin_kb())