from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from db import User
from tools import get_text_message

flags = {"throttling_key": "default"}
router = Router()


@router.message(flags=flags)
async def message_(
    message: Message,
    session: AsyncSession,
    state: FSMContext,
    user: User,
):
    await message.answer(text=await get_text_message("answer_on_unknown_message"))


@router.callback_query(flags=flags)
async def message_inline(
    query: CallbackQuery,
    session: AsyncSession,
    state: FSMContext,
    user: User,
):
    await query.message.delete_reply_markup()


# @router.message()
# async def message_(
#     message: Message,
#     session: AsyncSession,
#     state: FSMContext,
#     user: User,
# ):
#     # print(message.caption)
#     print(message.text)
