from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters import GetTextButton
from bot.keyboards import rk_admin_panel, rk_delete_post
from bot.states import AdminState
from db import PostInfo, User
from tools import editing, get_params_post_for_msg, get_text_message

flags = {"throttling_key": "default"}
router = Router()


@router.message(AdminState.admin_panel, GetTextButton("delete_post"), flags=flags)
async def delete_post_(
    message: Message,
    session: AsyncSession,
    state: FSMContext,
    user: User,
):
    posts_idpk = await session.scalars(
        select(PostInfo.idpk).where(PostInfo.is_sending_finished == True)  # noqa: E712
    )
    posts_idpk = posts_idpk.all()
    if not posts_idpk:
        await message.answer(
            text=await get_text_message("no_posts"),
        )
        return
    len_posts_idpk = len(posts_idpk)
    post = await session.get(PostInfo, posts_idpk[0])
    func, params = await get_params_post_for_msg(post, message)
    await func(**params)
    await message.answer(
        text=await get_text_message(
            "info_about_posts",
            total_posts=len_posts_idpk,
            post_id=1,
        ),
        reply_markup=await rk_delete_post(total_posts=len_posts_idpk),
    )
    await state.update_data(
        posts_idpk=posts_idpk,
        post_id=0,
        len_posts_idpk=len_posts_idpk,
    )
    await state.set_state(AdminState.delete_post)


@router.message(
    AdminState.delete_post,
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


@router.message(
    AdminState.delete_post,
    GetTextButton("next_post"),
    flags=flags,
)
async def next_post(
    message: Message,
    session: AsyncSession,
    state: FSMContext,
    user: User,
):
    data = await state.get_data()
    posts_idpk = data.get("posts_idpk")
    post_id = data.get("post_id")
    len_posts_idpk = data.get("len_posts_idpk")
    post_id += 1
    post = await session.get(PostInfo, posts_idpk[post_id])
    func, params = await get_params_post_for_msg(post, message)
    await func(**params)
    await message.answer(
        text=await get_text_message(
            "info_about_posts",
            total_posts=len_posts_idpk,
            post_id=post_id + 1,
        ),
        reply_markup=await rk_delete_post(total_posts=len_posts_idpk, post_id=post_id),
    )
    await state.update_data(
        post_id=post_id,
    )


@router.message(
    AdminState.delete_post,
    GetTextButton("prev_post"),
    flags=flags,
)
async def prev_post(
    message: Message,
    session: AsyncSession,
    state: FSMContext,
    user: User,
):
    data = await state.get_data()
    posts_idpk = data.get("posts_idpk")
    post_id = data.get("post_id")
    len_posts_idpk = data.get("len_posts_idpk")
    post_id -= 1
    post = await session.get(PostInfo, posts_idpk[post_id])
    func, params = await get_params_post_for_msg(post, message)
    await func(**params)
    await message.answer(
        text=await get_text_message(
            "info_about_posts",
            total_posts=len_posts_idpk,
            post_id=post_id + 1,
        ),
        reply_markup=await rk_delete_post(total_posts=len_posts_idpk, post_id=post_id),
    )
    await state.update_data(
        post_id=post_id,
    )


@router.message(
    AdminState.delete_post,
    GetTextButton("delete_post"),
    flags=flags,
)
async def process_delete_post(
    message: Message,
    session: AsyncSession,
    state: FSMContext,
    user: User,
):
    data = await state.get_data()
    posts_idpk = data.get("posts_idpk")
    post_id = data.get("post_id")
    post = await session.get(PostInfo, posts_idpk[post_id])

    await editing(session=session, bot=message.bot, post=post)

    await message.answer(
        text=await get_text_message("post_deleted"),
    )
    await state.set_state(AdminState.admin_panel)
    await message.answer(
        text=await get_text_message("admin_panel"),
        reply_markup=await rk_admin_panel(),
    )
