from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from db import User
from tools import get_text_message, get_photo_id

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


# @router.message()
# async def message_(
#     message: Message,
#     session: AsyncSession,
#     state: FSMContext,
#     user: User,
# ):
#     # print(message.caption)
#     print(message.text)