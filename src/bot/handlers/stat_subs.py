from datetime import datetime

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters import GetTextButton
from bot.states import AdminState
from db import Sub, User
from tools import get_text_message

flags = {"throttling_key": "default"}
router = Router()


@router.message(AdminState.admin_panel, GetTextButton("sub_statistics"), flags=flags)
async def stat_subs_(
    message: Message,
    session: AsyncSession,
    state: FSMContext,
    user: User,
):
    paid_subs = await session.scalars(
        select(Sub).where(
            and_(
                Sub.type_sub == "paid",
                Sub.sub_end_date > datetime.now(),
            )
        )
    )
    paid_subs = paid_subs.all()
    free_subs = await session.scalar(
        select(func.count())
        .select_from(Sub)
        .where(
            and_(
                Sub.type_sub == "free",
                Sub.sub_end_date > datetime.now(),
            )
        )
    )
    d = {}
    for paid_sub in paid_subs:
        user = await session.scalar(
            select(User).where(User.id_user == paid_sub.id_user)
        )
        if user.city in d:
            d[user.city] += 1
        else:
            d[user.city] = 1
    t = ""
    for city, count in d.items():
        t += await get_text_message(
            "pattern_sub_statistics_city",
            city=city,
            count=count,
        )
    await message.answer(
        text=await get_text_message(
            "sub_statistics",
            paid_subs=len(paid_subs),
            free_subs=free_subs,
            by_city=t,
        )
    )
