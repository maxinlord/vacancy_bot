from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters import GetTextButton
from db import User
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
    await message.answer(
        text=await get_text_message(
            "balance_info",
            end_date=user.sub_end_date.strftime("%d.%m.%Y"),
            city=user.city,
        )
    )
