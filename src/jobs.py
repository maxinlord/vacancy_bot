from datetime import datetime

from sqlalchemy import and_, select

import tools
from db import PostInfo, Sub, User
from init_bot import bot
from init_db import _sessionmaker_for_func


async def job_sec() -> None:
    now = datetime.now()
    second = now.second
    if second % 5 != 0:
        return
    async with _sessionmaker_for_func() as session:
        posts = await session.scalars(
            select(PostInfo).where(
                and_(
                    PostInfo.is_sending_finished == False,  # noqa: E712
                    PostInfo.is_sending_started == False,  # noqa: E712
                    PostInfo.date_start_sending <= datetime.now(),
                )
            )
        )
        for post in posts:
            post.is_sending_started = True
            await tools.mailing(session=session, bot=bot, post=post)


async def job_minute() -> None:
    pass


async def check_end_sub_day():
    async with _sessionmaker_for_func() as session:
        subs = await session.scalars(
            select(Sub).where(Sub.sub_end_date <= datetime.now())
        )
        for sub in subs:
            user = await session.scalar(select(User).where(User.id_user == sub.id_user))
            user.sub_active = False
        await session.commit()
