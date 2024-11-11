from datetime import datetime
from init_db import _sessionmaker_for_func
from db import PostInfo
from sqlalchemy import select, and_
from init_bot import bot
import tools


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
