from aiogram.utils.keyboard import ReplyKeyboardBuilder

import tools


async def rk_admin_cities():
    builder = ReplyKeyboardBuilder()
    builder.button(text=await tools.get_text_button("all_cities"))
    builder.button(text=await tools.get_text_button("city_1"))
    builder.button(text=await tools.get_text_button("city_2"))
    builder.button(text=await tools.get_text_button("city_3"))
    builder.button(text=await tools.get_text_button("back"))
    builder.adjust(1, 2, 1, 1)
    return builder.as_markup(resize_keyboard=True)


async def rk_done():
    builder = ReplyKeyboardBuilder()
    builder.button(text=await tools.get_text_button("done"))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)
