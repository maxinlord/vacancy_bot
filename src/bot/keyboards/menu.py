from aiogram.utils.keyboard import ReplyKeyboardBuilder

import tools


async def rk_main_menu():
    builder = ReplyKeyboardBuilder()
    builder.button(text=await tools.get_text_button("balance"))
    builder.button(text=await tools.get_text_button("change_city"))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)
