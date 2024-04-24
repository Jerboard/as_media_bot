
import db
import keyboards as kb
from init import bot
from utils.entities_utils import recover_entities


# отправить базовое сообщение
async def send_message(chat_id: int, wit_kb: bool = False):
    info = await db.get_info()
    entities = recover_entities(info.entities)
    keyboard = kb.get_main_user_kb() if wit_kb else None
    await bot.send_photo(
        chat_id=chat_id,
        photo=info.photo_id,
        caption=info.text,
        caption_entities=entities,
        parse_mode=None,
        reply_markup=keyboard
    )