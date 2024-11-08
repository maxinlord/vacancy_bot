from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from bot.states import AdminState

from bot.filters import GetTextButton
from bot.keyboards import rk_admin_panel, rk_main_menu
from db import User
from tools import get_text_message, is_admin

flags = {"throttling_key": "default"}
router = Router()


@router.message(GetTextButton("admin_panel"), flags=flags)
async def admin_panel_(
    message: Message,
    session: AsyncSession,
    state: FSMContext,
    user: User,
):
    if not is_admin(user.id_user):
        return
    await message.answer(
        text=await get_text_message("admin_panel"),
        reply_markup=await rk_admin_panel(),
    )
    await state.set_state(AdminState.admin_panel)


@router.message(AdminState.admin_panel, GetTextButton("back"), flags=flags)
async def back_to_main_menu(
    message: Message,
    session: AsyncSession,
    state: FSMContext,
    user: User,
):
    await state.clear()
    await message.answer(
        text=await get_text_message("main_menu"),
        reply_markup=await rk_main_menu(is_admin(user.id_user)),
    )
