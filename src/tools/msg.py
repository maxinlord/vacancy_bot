import asyncio
import json

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message
from aiogram.utils.media_group import MediaGroupBuilder
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

import tools
from config import ID_ADMIN
from db import PostInfo, PostMessage, User


async def mailing(session: AsyncSession, bot: Bot, post: PostInfo):
    if post.city == await tools.get_text_button("all_cities"):
        users = await session.scalars(
            select(User).where(
                and_(
                    User.bot_blocked == False,  # noqa
                    User.sub_active == True,  # noqa
                )
            )
        )
    else:
        users = await session.scalars(
            select(User).where(
                and_(
                    User.bot_blocked == False,  # noqa
                    User.sub_active == True,  # noqa
                    User.city == post.city,
                )
            )
        )
    users = users.all()
    func = None
    params = {}
    photo_id: list[str] = json.loads(post.photo_id)
    if not photo_id:
        func = bot.send_message
        params["text"] = post.text
    elif len(photo_id) == 1:
        func = bot.send_photo
        params["photo"] = photo_id[0]
        params["caption"] = post.text
    elif len(photo_id) > 1:
        func = bot.send_media_group
        media_group = MediaGroupBuilder(caption=post.text)
        for photo in photo_id:
            media_group.add(type="photo", media=photo)
        params["media"] = media_group.build()
    for user in users:
        try:
            msg = await func(chat_id=user.id_user, **params)
            session.add(
                PostMessage(
                    id_post=post.id_post,
                    id_user=user.id_user,
                    id_message=msg[0].message_id
                    if params.get("media")
                    else msg.message_id,
                )
            )
        except TelegramBadRequest:
            user.bot_blocked = True
        except Exception as e:
            print(e)
        await asyncio.sleep(0.04)
    post.is_sending_finished = True
    await session.commit()


async def get_params_post_for_msg(post: PostInfo, message: Message):
    photo_id = json.loads(post.photo_id)
    params = {}
    func = None
    if photo_id:
        params["caption"] = post.text
        if len(photo_id) == 1:
            func = message.answer_photo
            params["photo"] = photo_id[0]
        else:
            func = message.answer_media_group
            media_group = MediaGroupBuilder(caption=post.text)
            for photo in photo_id:
                media_group.add(type="photo", media=photo)
            params["media"] = media_group.build()
    else:
        func = message.answer
        params["text"] = post.text
    return func, params


async def editing(session: AsyncSession, bot: Bot, post: PostInfo):
    post_messages = await session.scalars(
        select(PostMessage).where(PostMessage.id_post == post.id_post)
    )
    post_messages = post_messages.all()
    photo_id: list[str] = json.loads(post.photo_id)
    for post_message in post_messages:
        try:
            if photo_id and len(photo_id) > 1:
                await bot.delete_messages(
                    chat_id=post_message.id_user,
                    message_ids=[
                        post_message.id_message + i for i in range(len(photo_id))
                    ],
                )
            else:
                await bot.delete_message(
                    chat_id=post_message.id_user, message_id=post_message.id_message
                )
        except TelegramBadRequest as t:
            if t.message == "Bad Request: message to delete not found":
                await session.delete(post_message)
                continue
            await bot.send_message(
                chat_id=ID_ADMIN[0],
                text=await tools.get_text_message("error_delete_message", e=t.message),
            )
            try:
                text = await tools.get_text_message("dot")
                if not photo_id:
                    await bot.edit_message_text(
                        chat_id=post_message.id_user,
                        message_id=post_message.id_message,
                        text=text,
                    )
                else:
                    await bot.edit_message_caption(
                        chat_id=post_message.id_user,
                        message_id=post_message.id_message,
                        caption=text,
                    )
            except TelegramBadRequest as t:
                await bot.send_message(
                    chat_id=ID_ADMIN[0],
                    text=await tools.get_text_message(
                        "error_edit_message", e=t.message
                    ),
                )
        except Exception as e:
            await bot.send_message(
                chat_id=ID_ADMIN[0],
                text=await tools.get_text_message("unknown_error", e=e),
            )
        await session.delete(post_message)
        await asyncio.sleep(0.04)
    await session.delete(post)
    await session.commit()
