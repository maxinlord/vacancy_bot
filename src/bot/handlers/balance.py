from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters import GetTextButton
from db import User, Sub
from tools import (
    get_text_message,
)

flags = {"throttling_key": "default"}
router = Router()


@router.message(GetTextButton("balance"), flags=flags)
async def balance_info(
    message: Message,
    session: AsyncSession,
    state: FSMContext,
    user: User,
):
    sub = await session.scalar(
        select(Sub).where(Sub.id_user == user.id_user).order_by(Sub.sub_end_date.desc())
    )
    await message.answer(
        text=await get_text_message(
            "balance_info",
            end_date=sub.sub_end_date.strftime("%d.%m.%Y"),
            city=user.city,
        )
    )
