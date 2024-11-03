from aiogram.utils.keyboard import ReplyKeyboardBuilder

import tools


async def rk_registration():
    builder = ReplyKeyboardBuilder()
    builder.button(text=await tools.get_text_button("registration"))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


async def rk_cities():
    builder = ReplyKeyboardBuilder()
    builder.button(text=await tools.get_text_button("city_1"))
    builder.button(text=await tools.get_text_button("city_2"))
    builder.button(text=await tools.get_text_button("city_3"))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


async def rk_accept_terms():
    builder = ReplyKeyboardBuilder()
    builder.button(text=await tools.get_text_button("accept_terms"))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)