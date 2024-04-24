import sqlalchemy as sa
import typing as t

from datetime import date, datetime
from sqlalchemy.dialects import postgresql as psql

from init import TZ
from db.base import METADATA, begin_connection


class MediaRow(t.Protocol):
    id: int
    created_at: datetime
    media_group_id: str
    file_id: str
    text: str
    entities: list[str]


MediaTable = sa.Table(
    'media_group_cache',
    METADATA,
    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('created_at', sa.DateTime(timezone=True), default=datetime.now(TZ)),
    sa.Column('media_group_id', sa.String),
    sa.Column('file_id', sa.String(255)),
    sa.Column('text', sa.Text),
    sa.Column('entities', sa.ARRAY(sa.String)),
)


# добавить запись в кэш медиа группы
async def add_media_group_cache(media_group_id: str, file_id: str, text: str, entities: list[str]):
    now = datetime.now(TZ).replace(microsecond=0)
    query = MediaTable.insert().values(
        media_group_id=media_group_id,
        created_at=now,
        file_id=file_id,
        text=text,
        entities=entities,
    )
    async with begin_connection() as conn:
        await conn.execute(query)


# возвращает все записи из кэша медиа группы
async def get_all_media_group_cache(media_group_id: str) -> tuple[MediaRow]:
    query = MediaTable.select().where(MediaTable.c.media_group_id == media_group_id)
    async with begin_connection() as conn:
        result = await conn.execute(query)
    return result.all()


# удаляет все записи медиагруппы из кэша
async def del_media_group_cache(media_group_id: str):
    query = MediaTable.delete().where(MediaTable.c.media_group_id == media_group_id)
    async with begin_connection() as conn:
        await conn.execute(query)