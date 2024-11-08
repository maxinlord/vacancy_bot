from aiogram.utils.keyboard import ReplyKeyboardBuilder

import tools


async def rk_main_menu(is_admin: bool):
    builder = ReplyKeyboardBuilder()
    builder.button(text=await tools.get_text_button("balance"))
    builder.button(text=await tools.get_text_button("change_city"))
    if is_admin:
        builder.button(text=await tools.get_text_button("admin_panel"))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


async def rk_admin_panel():
    builder = ReplyKeyboardBuilder()
    builder.button(text=await tools.get_text_button("user_statistics"))
    builder.button(text=await tools.get_text_button("sub_statistics"))
    builder.button(text=await tools.get_text_button("post_statistics"))
    builder.button(text=await tools.get_text_button("delete_post"))
    builder.button(text=await tools.get_text_button("load_post"))
    builder.button(text=await tools.get_text_button("back"))
    builder.adjust(1, 2, 2, 1)
    return builder.as_markup(resize_keyboard=True)
