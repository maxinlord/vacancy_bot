import random
import string
from datetime import timedelta

from aiogram.types import Message

from config import ID_ADMIN


def is_admin(id_user: int):
    return id_user == ID_ADMIN


def parser_str_to_timedelta(time_str: str) -> timedelta | None:
    if not time_str:
        return None
    letter_time = time_str[-1]
    _ = time_str[:-1]
    if not _.isdigit():
        return None
    num = int(_)
    if letter_time == "d":
        return timedelta(days=num)
    elif letter_time == "h":
        return timedelta(hours=num)
    elif letter_time == "m":
        return timedelta(minutes=num)
    elif letter_time == "s":
        return timedelta(seconds=num)
    return None


def get_photo_id(message: Message) -> str | None:
    return message.photo[-1].file_id if message.photo else None


def collapse_collision_media_OLD(posts: list):
    new_posts = []
    media_group = []
    c_posts = posts.copy()
    for post in posts:
        if not post:
            continue
        if not post.get("photo_id"):
            new_posts.append(post)
            c_posts.remove(post)
            continue
        text = post["text"]
        counter = 0
        while counter < len(c_posts):
            c_post = c_posts[counter]
            if text == c_post["text"] and c_post.get("photo_id"):
                media_group.append(c_post["photo_id"])
                c_posts.remove(c_post)
                ind_for_edit = posts.index(c_post)
                posts[ind_for_edit] = {}
            else:
                counter += 1

        new_posts.append({"text": text, "photo_id": media_group})
        media_group = []
        if not c_posts:
            break
    return new_posts


def collapse_collision_media(posts: list):
    new_posts = []
    media_group = []
    c_posts = posts.copy()
    for post in posts:
        if not post:
            continue
        if not post.get("photo_id"):
            new_posts.append(post)
            c_posts.remove(post)
            continue
        text = post["text"]
        for ind_c_post, c_post in enumerate(c_posts):
            if not c_post:
                continue
            if text == c_post["text"] and c_post.get("photo_id"):
                media_group.append(c_post["photo_id"])
                c_posts[ind_c_post] = {}
                ind_for_edit = posts.index(c_post)
                posts[ind_for_edit] = {}

        new_posts.append({"text": text, "photo_id": media_group})
        media_group = []
        if not c_posts:
            break
    return new_posts



def gen_key(length: int):
    return "".join(
        random.choice(string.ascii_letters + string.digits) for _ in range(length)
    )
