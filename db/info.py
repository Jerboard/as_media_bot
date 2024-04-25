import sqlalchemy as sa
import typing as t

from datetime import date, datetime
from sqlalchemy.dialects import postgresql as psql

from init import TZ
from db.base import METADATA, begin_connection


class InfoRow(t.Protocol):
    id: int
    updated_at: datetime
    photo_id: str
    text: str
    entities: list[str]


InfoTable = sa.Table(
    'info',
    METADATA,
    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), default=datetime.now(TZ), onupdate=datetime.now(TZ)),
    sa.Column('photo_id', sa.String(255)),
    sa.Column('text', sa.String(255)),
    sa.Column('entities', sa.ARRAY(sa.String(255)))
)


# обновить инфо
async def update_info(
        photo_id: str = None,
        text: str = None,
        entities: list = None
) -> None:
    now = datetime.now(TZ).replace(microsecond=0)
    query = InfoTable.update().where(InfoTable.c.id == 1).values(updated_at=now)

    if photo_id:
        query = query.values(photo_id=photo_id)
    if text:
        query = query.values(text=text, entities=entities)

    async with begin_connection() as conn:
        await conn.execute(query)


# получить инфо
async def get_info() -> InfoRow:
    query = InfoTable.select().where(InfoTable.c.id == 1)
    async with begin_connection() as conn:
        result = await conn.execute(query)
    return result.first()
