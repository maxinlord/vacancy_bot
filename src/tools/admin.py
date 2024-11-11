import random
import string
from datetime import datetime, timedelta

from aiogram.types import Message

from config import ID_ADMIN


def is_admin(id_user: int):
    return id_user == ID_ADMIN


def get_days_in_month(now: datetime):
    month = now.month
    year = now.year
    if month == 12:
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year
    return (datetime(next_year, next_month, 1) - timedelta(days=1)).day


def parser_str_to_timedelta(time_str: str) -> timedelta | None:
    if not time_str:
        return None
    letter_time = time_str[-1]
    _ = time_str[:-1]
    if not _.isdigit():
        return None
    num = int(_)
    if letter_time in ["d", "д"]:
        return timedelta(days=num)
    elif letter_time in ["h", "ч"]:
        return timedelta(hours=num)
    elif letter_time in ["m", "м"]:
        return timedelta(minutes=num)
    elif letter_time in ["s", "с"]:
        return timedelta(seconds=num)
    return None


def get_photo_id(message: Message) -> str | None:
    return message.photo[-1].file_id if message.photo else None


def gen_key(length: int):
    return "".join(
        random.choice(string.ascii_letters + string.digits) for _ in range(length)
    )
