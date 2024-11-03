from aiogram import F, Router
from aiogram.filters import CommandObject, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters import GetTextButton
from bot.keyboards import rk_accept_terms, rk_cities, rk_main_menu, rk_registration
from bot.states import UserState
from db import User
from tools import get_text_message, get_text_button

router = Router()


@router.message(CommandStart())
async def cmd_start(
    message: Message,
    command: CommandObject,
    session: AsyncSession,
    state: FSMContext,
    user: User | None,
):
    await message.answer(
        text=await get_text_message(
            "start_greeting", name_user=message.from_user.full_name
        ),
        reply_markup=await rk_registration(),
    )
    await state.set_state(UserState.start_registration)


@router.message(UserState.start_registration, GetTextButton("registration"))
async def start_registration(
    message: Message,
    session: AsyncSession,
    state: FSMContext,
    user: User | None,
):
    await message.answer(
        text=await get_text_message("pick_one_of_city"), reply_markup=await rk_cities()
    )
    await state.set_state(UserState.pick_city)


@router.message(UserState.pick_city)
async def get_city(
    message: Message,
    session: AsyncSession,
    state: FSMContext,
    user: User | None,
):
    cities = []
    for x in range(1, 4):
        cities.append(await get_text_button(f"city_{x}"))
    if message.text not in cities:
        return
    await message.answer(
        text=await get_text_message("sub_info_and_bot_policy", price_sub=100),
        reply_markup=await rk_accept_terms(),
    )
    await state.set_state(UserState.accept_terms)


@router.message(UserState.accept_terms, GetTextButton("accept_terms"))
async def accept_terms(
    message: Message,
    session: AsyncSession,
    state: FSMContext,
    user: User | None,
):
    await message.answer(
        text=await get_text_message("thanks"), reply_markup=await rk_main_menu()
    )
    await state.clear()


@router.message(CommandStart(deep_link=True))
async def cmd_start_with_deep_link(
    message: Message,
    command: CommandObject,
    session: AsyncSession,
    state: FSMContext,
    user: User | None,
):
    pass
