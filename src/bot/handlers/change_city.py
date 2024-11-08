from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters import GetTextButton
from bot.keyboards import rk_cities, rk_main_menu
from bot.states import UserState
from db import User
from tools import get_cities, get_text_message, is_admin

flags = {"throttling_key": "default"}
router = Router()


@router.message(GetTextButton("change_city"), flags=flags)
async def pick_one_of_city_to_edit(
    message: Message,
    session: AsyncSession,
    state: FSMContext,
    user: User,
):
    await message.answer(
        text=await get_text_message("pick_one_of_city_to_edit"),
        reply_markup=await rk_cities(),
    )
    await state.set_state(UserState.pick_city_to_edit)


@router.message(UserState.pick_city_to_edit, flags=flags)
async def get_another_city(
    message: Message,
    session: AsyncSession,
    state: FSMContext,
    user: User,
):
    if message.text not in await get_cities():
        return
    user.city = message.text
    await message.answer(
        text=await get_text_message("city_updated"),
        reply_markup=await rk_main_menu(is_admin(user.id_user)),
    )
    await session.commit()
    await state.clear()
