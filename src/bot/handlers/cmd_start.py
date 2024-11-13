from datetime import datetime, timedelta

from aiogram import Router
from aiogram.filters import CommandObject, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters import GetTextButton
from bot.keyboards import rk_accept_terms, rk_cities, rk_main_menu, rk_registration
from bot.states import UserState
from db import User, Sub
from tools import get_cities, get_text_message, get_value, is_admin

flags = {"throttling_key": "default"}
router = Router()


@router.message(CommandStart(), flags=flags)
async def cmd_start(
    message: Message,
    command: CommandObject,
    session: AsyncSession,
    state: FSMContext,
    user: User,
):
    if user.city:
        return await message.answer(
            text=await get_text_message("main_menu"),
            reply_markup=await rk_main_menu(is_admin(user.id_user)),
        )
    await message.answer(
        text=await get_text_message(
            "start_greeting", name_user=message.from_user.full_name
        ),
        reply_markup=await rk_registration(),
    )
    await state.set_state(UserState.start_registration)


@router.message(
    UserState.start_registration, GetTextButton("registration"), flags=flags
)
async def start_registration(
    message: Message,
    session: AsyncSession,
    state: FSMContext,
    user: User,
):
    await message.answer(
        text=await get_text_message("pick_one_of_city"), reply_markup=await rk_cities()
    )
    await state.set_state(UserState.pick_city)


@router.message(UserState.pick_city, flags=flags)
async def get_city(
    message: Message,
    session: AsyncSession,
    state: FSMContext,
    user: User,
):
    if message.text not in await get_cities():
        return
    FREE_SUB_DAYS = await get_value(session=session, value_name="FREE_SUB_DAYS")
    PRICE_SUB = await get_value(session=session, value_name="PRICE_SUB", cache_=False)
    sub_end_date = datetime.now() + timedelta(days=FREE_SUB_DAYS)
    await message.answer(
        text=await get_text_message(
            "sub_info_and_bot_policy",
            price_sub=PRICE_SUB,
            free_sub_days=FREE_SUB_DAYS,
            sub_end_date=sub_end_date.strftime("%d.%m.%Y"),
        ),
        reply_markup=await rk_accept_terms(),
    )
    user.city = message.text
    session.add(
        Sub(
            id_user=user.id_user,
            id_sub=0,
            type_sub="free",
            sub_start_date=datetime.now(),
            sub_end_date=sub_end_date,
            days=FREE_SUB_DAYS,
            price=PRICE_SUB,
        )
    )
    user.sub_active = True
    await session.commit()
    await state.set_state(UserState.accept_terms)


@router.message(UserState.accept_terms, GetTextButton("accept_terms"), flags=flags)
async def accept_terms(
    message: Message,
    session: AsyncSession,
    state: FSMContext,
    user: User,
):
    await message.answer(
        text=await get_text_message("thanks"),
        reply_markup=await rk_main_menu(is_admin(user.id_user)),
    )
    await state.clear()


@router.message(CommandStart(deep_link=True))
async def cmd_start_with_deep_link(
    message: Message,
    command: CommandObject,
    session: AsyncSession,
    state: FSMContext,
    user: User,
):
    pass
