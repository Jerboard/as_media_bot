import sqlalchemy as sa
import typing as t

from datetime import date, datetime
from sqlalchemy.dialects import postgresql as psql

from init import TZ
from db.base import METADATA, begin_connection


class UserRow(t.Protocol):
    id: int
    created_at: datetime
    updated_at: datetime
    user_id: int
    full_name: str
    username: str
    phone: str


UserTable = sa.Table(
    'users',
    METADATA,
    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('created_at', sa.DateTime(timezone=True), default=datetime.now(TZ)),
    sa.Column('updated_at', sa.DateTime(timezone=True), default=datetime.now(TZ), onupdate=datetime.now(TZ)),
    sa.Column('user_id', sa.BigInteger, unique=True),
    sa.Column('full_name', sa.String(255)),
    sa.Column('username', sa.String(255)),
    sa.Column('phone', sa.String(255))
)


# создаёт или обновляет пользователя
async def create_or_update_user(
        user_id: int,
        full_name: str,
        username: str
) -> None:
    now = datetime.now(TZ).replace(microsecond=0)
    query = (
        psql.insert(UserTable)
        .values(
            created_at=now,
            updated_at=now,
            user_id=user_id,
            full_name=full_name,
            username=username,
        )
        .on_conflict_do_update(
            index_elements=[UserTable.c.user_id],
            set_={"updated_at": now,
                  "full_name": full_name,
                  "username": username,
                  }
        )
    )
    async with begin_connection() as conn:
        await conn.execute(query)


# обновляет данные пользователя
async def update_user(user_id: int, phone: str = None) -> None:
    query = UserTable.update().where(UserTable.c.user_id == user_id).values(updated_at=datetime.now(TZ))

    if phone:
        query = query.values(phone=phone)

    async with begin_connection() as conn:
        await conn.execute(query)


# получить пользователей
async def get_users(with_phone: bool = None, all_users: bool = False) -> list[UserRow]:
    query = UserTable.select()

    if not all_users:
        if with_phone:
            query = query.where(UserTable.c.phone.isnot(None))
        else:
            query = query.where(UserTable.c.phone.is_(None))

    async with begin_connection() as conn:
        result = await conn.execute(query)
    return result.all()