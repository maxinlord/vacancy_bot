import tools
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


async def ik_back(custom_callback_data: str = "back"):
    builder = InlineKeyboardBuilder()
    builder.button(
        text=await tools.get_text_button("back"), callback_data=custom_callback_data
    )
    return builder.as_markup()


async def rk_back():
    builder = ReplyKeyboardBuilder()
    builder.button(text=await tools.get_text_button("back"))
    return builder.as_markup(resize_keyboard=True)
