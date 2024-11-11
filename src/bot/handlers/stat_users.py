from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters import GetTextButton
from bot.states import AdminState
from db import User
from tools import get_text_button, get_text_message

flags = {"throttling_key": "default"}
router = Router()


@router.message(AdminState.admin_panel, GetTextButton("user_statistics"), flags=flags)
async def stat_users_(
    message: Message,
    session: AsyncSession,
    state: FSMContext,
    user: User,
):
    total_users = await session.scalar(select(func.count()).select_from(User))
    blocked_bot_users = await session.scalar(
        select(func.count()).select_from(User).where(User.bot_blocked == True)  # noqa: E712
    )
    city_1_users = await session.scalar(
        select(func.count())
        .select_from(User)
        .where(User.city == await get_text_button("city_1"))
    )
    city_2_users = await session.scalar(
        select(func.count())
        .select_from(User)
        .where(User.city == await get_text_button("city_2"))
    )
    city_3_users = await session.scalar(
        select(func.count())
        .select_from(User)
        .where(User.city == await get_text_button("city_3"))
    )
    await message.answer(
        await get_text_message(
            "stat_users",
            total_users=total_users,
            blocked_bot_users=blocked_bot_users,
            city_1_users=city_1_users,
            city_2_users=city_2_users,
            city_3_users=city_3_users,
        )
    )
