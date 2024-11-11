from aiogram.utils.keyboard import (
    ReplyKeyboardBuilder,
)

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


async def rk_delete_post(
    total_posts: int,
    post_id: int = 0,
):
    post_id += 1
    builder = ReplyKeyboardBuilder()
    builder.button(
        text=await tools.get_text_button("delete_post"),
    )
    q_bttn = 0
    if post_id > 1:
        builder.button(
            text=await tools.get_text_button("prev_post"),
        )
        q_bttn += 1
    if post_id < total_posts:
        builder.button(
            text=await tools.get_text_button("next_post"),
        )
        q_bttn += 1
    builder.button(
        text=await tools.get_text_button("back"),
    )
    if not q_bttn:
        builder.adjust(1, 1)
    else:
        builder.adjust(1, q_bttn, 1)
    return builder.as_markup(resize_keyboard=True)


async def rk_time_stat_posts():
    builder = ReplyKeyboardBuilder()
    builder.button(text=await tools.get_text_button("one_day"))
    builder.button(text=await tools.get_text_button("one_week"))
    builder.button(text=await tools.get_text_button("one_month"))
    builder.button(text=await tools.get_text_button("one_year"))
    builder.button(text=await tools.get_text_button("back"))
    builder.adjust(2, 2, 1)
    return builder.as_markup(resize_keyboard=True)
