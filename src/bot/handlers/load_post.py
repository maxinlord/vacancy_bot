import json
from datetime import datetime

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters import GetTextButton
from bot.keyboards import rk_admin_cities, rk_admin_panel, rk_done
from bot.middlewares import AlbumMiddleware
from bot.states import AdminState
from db import PostInfo, User
from tools import (
    gen_key,
    get_cities,
    get_photo_id,
    get_text_button,
    get_text_message,
    parser_str_to_timedelta,
)

flags = {"throttling_key": "default"}
router = Router()

router.message.middleware(AlbumMiddleware(latency=1))


@router.message(AdminState.admin_panel, GetTextButton("load_post"), flags=flags)
async def load_post_(
    message: Message,
    session: AsyncSession,
    state: FSMContext,
    user: User,
):
    await message.answer(
        text=await get_text_message("pick_city_for_post"),
        reply_markup=await rk_admin_cities(),
    )
    await state.clear()
    await state.set_state(AdminState.pick_city_for_post)


@router.message(
    AdminState.pick_city_for_post,
    GetTextButton("back"),
    flags=flags,
)
async def back_to_panel(
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


@router.message(AdminState.pick_city_for_post, flags=flags)
async def delay_between_posts(
    message: Message,
    session: AsyncSession,
    state: FSMContext,
    user: User,
):
    if message.text not in await get_cities():
        if message.text != await get_text_button("all_cities"):
            return
    await state.update_data(city=message.text)
    await message.answer(
        text=await get_text_message("delay_between_posts"),
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(AdminState.delay_between_posts)


@router.message(AdminState.delay_between_posts, flags=flags)
async def wait_posts(
    message: Message,
    session: AsyncSession,
    state: FSMContext,
    user: User,
):
    if not parser_str_to_timedelta(message.text):
        await message.answer(
            text=await get_text_message("error_not_valid_delay"),
        )
        return
    await state.update_data(delay=message.text)
    await message.answer(
        text=await get_text_message("send_posts_to_mailing"),
    )
    await state.set_state(AdminState.wait_posts)


@router.message(AdminState.wait_posts, GetTextButton("done"), flags=flags)
async def done(
    message: Message,
    session: AsyncSession,
    state: FSMContext,
    user: User,
):
    data = await state.get_data()
    posts = data["posts"]
    now = datetime.now()
    delay = parser_str_to_timedelta(data["delay"])
    for post in posts:
        session.add(
            PostInfo(
                id_post=gen_key(12),
                city=data["city"],
                date_load=datetime.now(),
                date_start_sending=now,
                text=post["text"],
                photo_id=json.dumps(post.get("photo_id", [])),
            )
        )
        now += delay
    await session.commit()
    await message.answer(
        text=await get_text_message("sending_has_started"),
        reply_markup=await rk_admin_panel(),
    )
    await state.set_state(AdminState.admin_panel)


@router.message(AdminState.wait_posts)
async def get_posts(
    message: Message,
    session: AsyncSession,
    state: FSMContext,
    user: User,
    album: list[Message] | None = None,
):
    data = await state.get_data()
    posts = data.get("posts", [])

    if album:
        text = album[0].caption
        photo_id = [get_photo_id(msg) for msg in album]
        posts.append({"photo_id": photo_id, "text": text})
    elif photo_id := get_photo_id(message):
        posts.append({"photo_id": [photo_id], "text": message.caption})
    else:
        posts.append({"text": message.text})
    amount_posts = len(posts)
    await message.answer(
        text=await get_text_message("posts_loaded", amount_posts=amount_posts),
        reply_markup=await rk_done(),
    )
    await state.update_data(posts=posts)
