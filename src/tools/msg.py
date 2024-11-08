import asyncio
from aiogram.types import Message
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db import User
import tools


async def mailing(session: AsyncSession, message: Message):
    users = await session.scalars(select(User))
    users = users.all()
    not_sended = []
    for user in users:
        try:
            await message.send_copy(chat_id=user.id_user)
        except Exception:
            not_sended.append(user.id_user)
        await asyncio.sleep(0.5)
    amount_got_message = len(users) - len(not_sended)
    amount_not_got_message = len(not_sended)
    not_sended = ", ".join(not_sended) if not_sended else "Нет"
    await message.answer(
        text=await tools.get_text_message(
            "mess_mailing_finish",
            amount_got_message=amount_got_message,
            amount_not_got_message=amount_not_got_message,
            not_sended=not_sended,
        )
    )
