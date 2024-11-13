import contextlib
from datetime import datetime, timedelta

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, PreCheckoutQuery
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters import GetTextButton
from config import PAYMENT_TOKEN
from db import Sub, User
from init_db import _sessionmaker_for_func
from tools import gen_key, get_text_message, get_value

flags = {"throttling_key": "default"}
router = Router()


@router.message(GetTextButton("balance"), flags=flags)
async def balance_info(
    message: Message,
    session: AsyncSession,
    state: FSMContext,
    user: User,
):
    sub = await session.scalar(
        select(Sub).where(Sub.id_user == user.id_user).order_by(Sub.sub_end_date.desc())
    )
    if user.sub_active:
        await message.answer(
            text=await get_text_message(
                "balance_info",
                end_date=sub.sub_end_date.strftime("%d.%m.%Y"),
                city=user.city,
            )
        )
        return
    PRICE_SUB = await get_value(session=session, value_name="PRICE_SUB", cache_=False)
    msg = await message.answer(text=await get_text_message("sub_ended"))
    await message.answer_invoice(
        title=await get_text_message("invoice_title"),
        description=await get_text_message("invoice_description"),
        payload=f"{msg.message_id+1}",
        provider_token=PAYMENT_TOKEN,
        currency="RUB",
        prices=[
            {
                "label": await get_text_message("invoice_label"),
                "amount": PRICE_SUB * 100,
            }
        ],
    )


@router.pre_checkout_query()
async def on_pre_checkout_query(
    pre_checkout_query: PreCheckoutQuery,
):
    async with _sessionmaker_for_func() as session:
        PRICE_SUB = await get_value(
            session=session, value_name="PRICE_SUB", cache_=False
        )
    if pre_checkout_query.total_amount != PRICE_SUB * 100:
        await pre_checkout_query.answer(
            ok=False,
            error_message=await get_text_message("invoice_message_error"),
        )
        with contextlib.suppress(Exception):
            await pre_checkout_query.bot.delete_message(
                chat_id=pre_checkout_query.from_user.id,
                message_id=pre_checkout_query.invoice_payload,
            )
        return
    await pre_checkout_query.answer(ok=True)


@router.message(F.successful_payment)
async def on_successful_payment(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
    user: User | None,
):
    PRICE_SUB = message.successful_payment.total_amount // 100
    days = 30
    session.add(
        Sub(
            id_user=user.id_user,
            id_sub=gen_key(11),
            type_sub="paid",
            sub_start_date=datetime.now(),
            sub_end_date=datetime.now() + timedelta(days=days),
            days=days,
            price=PRICE_SUB,
        )
    )
    user.sub_active = True
    await session.commit()
    with contextlib.suppress(Exception):
        await message.bot.delete_message(
            chat_id=message.from_user.id,
            message_id=message.successful_payment.invoice_payload,
        )
    await message.answer(text=await get_text_message("invoice_message_success"))
