from datetime import datetime, timedelta

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters import GetTextButton
from bot.keyboards import rk_admin_panel, rk_time_stat_posts
from bot.states import AdminState
from db import PostInfo, User
from tools import get_days_in_month, get_text_message

flags = {"throttling_key": "default"}
router = Router()


@router.message(
    AdminState.admin_panel,
    GetTextButton("post_statistics"),
    flags=flags,
)
async def stat_posts_(
    message: Message,
    session: AsyncSession,
    state: FSMContext,
    user: User,
):
    posted_post = await session.scalar(
        select(func.count())
        .select_from(PostInfo)
        .where(
            PostInfo.is_sending_finished == True,  # noqa
        )
    )
    waiting_post = await session.scalar(
        select(func.count())
        .select_from(PostInfo)
        .where(
            and_(
                PostInfo.is_sending_started == False,  # noqa
                PostInfo.is_sending_finished == False,  # noqa
            )
        )
    )
    await state.set_state(AdminState.post_statistics)
    await message.answer(
        text=await get_text_message(
            "stat_posts",
            posted_post=posted_post,
            waiting_post=waiting_post,
        ),
        reply_markup=await rk_time_stat_posts(),
    )


@router.message(AdminState.post_statistics, GetTextButton("back"), flags=flags)
async def bact_to_admin_panel_from_stat_posts(
    message: Message,
    session: AsyncSession,
    state: FSMContext,
    user: User,
):
    await state.set_state(AdminState.admin_panel)
    await message.answer(
        text=await get_text_message("admin_panel"),
        reply_markup=await rk_admin_panel(),
    )


@router.message(AdminState.post_statistics, GetTextButton("one_day"), flags=flags)
async def stat_posts_one_day(
    message: Message,
    session: AsyncSession,
    state: FSMContext,
    user: User,
):
    now = datetime.now()
    start_time = datetime(
        year=now.year,
        month=now.month,
        day=now.day,
        hour=0,
        minute=0,
        second=0,
    )
    end_time = datetime(
        year=now.year,
        month=now.month,
        day=now.day,
        hour=23,
        minute=59,
        second=59,
    )
    posted_post = await session.scalar(
        select(func.count())
        .select_from(PostInfo)
        .where(
            and_(
                PostInfo.is_sending_finished == True,  # noqa
                PostInfo.date_start_sending >= start_time,
                PostInfo.date_start_sending <= end_time,
            )
        )
    )
    waiting_post = await session.scalar(
        select(func.count())
        .select_from(PostInfo)
        .where(
            and_(
                PostInfo.is_sending_finished == False,  # noqa
                PostInfo.is_sending_started == False,  # noqa
                PostInfo.date_start_sending >= start_time,
                PostInfo.date_start_sending <= end_time,
            )
        )
    )
    await message.answer(
        text=await get_text_message(
            "stat_posts_one_day",
            posted_post=posted_post,
            waiting_post=waiting_post,
            start_time=start_time.strftime("%d.%m.%Y %H:%M:%S"),
            end_time=end_time.strftime("%d.%m.%Y %H:%M:%S"),
        ),
    )


@router.message(AdminState.post_statistics, GetTextButton("one_week"), flags=flags)
async def stat_posts_one_week(
    message: Message,
    session: AsyncSession,
    state: FSMContext,
    user: User,
):
    now = datetime.now()
    start_of_weekday = now - timedelta(days=now.weekday())
    start_of_weekday = start_of_weekday.replace(hour=0, minute=0, second=0)
    end_of_weekday = start_of_weekday + timedelta(
        days=6, hours=23, minutes=59, seconds=59
    )

    posted_post = await session.scalar(
        select(func.count())
        .select_from(PostInfo)
        .where(
            and_(
                PostInfo.is_sending_finished == True,  # noqa
                PostInfo.date_start_sending >= start_of_weekday,
                PostInfo.date_start_sending <= end_of_weekday,
            )
        )
    )
    waiting_post = await session.scalar(
        select(func.count())
        .select_from(PostInfo)
        .where(
            and_(
                PostInfo.is_sending_finished == False,  # noqa
                PostInfo.is_sending_started == False,  # noqa
                PostInfo.date_start_sending >= start_of_weekday,
                PostInfo.date_start_sending <= end_of_weekday,
            )
        )
    )
    await message.answer(
        text=await get_text_message(
            "stat_posts_one_week",
            posted_post=posted_post,
            waiting_post=waiting_post,
            start_time=start_of_weekday.strftime("%d.%m.%Y %H:%M:%S"),
            end_time=end_of_weekday.strftime("%d.%m.%Y %H:%M:%S"),
        ),
    )


@router.message(AdminState.post_statistics, GetTextButton("one_month"), flags=flags)
async def stat_posts_one_month(
    message: Message,
    session: AsyncSession,
    state: FSMContext,
    user: User,
):
    now = datetime.now()
    start_time = datetime(
        year=now.year,
        month=now.month,
        day=1,
        hour=0,
        minute=0,
        second=0,
    )
    end_time = datetime(
        year=now.year,
        month=now.month,
        day=get_days_in_month(now),
        hour=23,
        minute=59,
        second=59,
    )
    posted_post = await session.scalar(
        select(func.count())
        .select_from(PostInfo)
        .where(
            and_(
                PostInfo.is_sending_finished == True,  # noqa
                PostInfo.date_start_sending >= start_time,
                PostInfo.date_start_sending <= end_time,
            )
        )
    )
    waiting_post = await session.scalar(
        select(func.count())
        .select_from(PostInfo)
        .where(
            and_(
                PostInfo.is_sending_finished == False,  # noqa
                PostInfo.is_sending_started == False,  # noqa
                PostInfo.date_start_sending >= start_time,
                PostInfo.date_start_sending <= end_time,
            )
        )
    )
    await message.answer(
        text=await get_text_message(
            "stat_posts_one_month",
            posted_post=posted_post,
            waiting_post=waiting_post,
            start_time=start_time.strftime("%d.%m.%Y %H:%M:%S"),
            end_time=end_time.strftime("%d.%m.%Y %H:%M:%S"),
        ),
    )


@router.message(AdminState.post_statistics, GetTextButton("one_year"), flags=flags)
async def stat_posts_one_year(
    message: Message,
    session: AsyncSession,
    state: FSMContext,
    user: User,
):
    now = datetime.now()
    start_time = datetime(
        year=now.year,
        month=1,
        day=1,
        hour=0,
        minute=0,
        second=0,
    )
    end_time = datetime(
        year=now.year,
        month=12,
        day=31,
        hour=23,
        minute=59,
        second=59,
    )
    posted_post = await session.scalar(
        select(func.count())
        .select_from(PostInfo)
        .where(
            and_(
                PostInfo.is_sending_finished == True,  # noqa
                PostInfo.date_start_sending >= start_time,
                PostInfo.date_start_sending <= end_time,
            )
        )
    )
    waiting_post = await session.scalar(
        select(func.count())
        .select_from(PostInfo)
        .where(
            and_(
                PostInfo.is_sending_finished == False,  # noqa
                PostInfo.is_sending_started == False,  # noqa
                PostInfo.date_start_sending >= start_time,
                PostInfo.date_start_sending <= end_time,
            )
        )
    )
    await message.answer(
        text=await get_text_message(
            "stat_posts_one_year",
            posted_post=posted_post,
            waiting_post=waiting_post,
            start_time=start_time.strftime("%d.%m.%Y %H:%M:%S"),
            end_time=end_time.strftime("%d.%m.%Y %H:%M:%S"),
        ),
    )
