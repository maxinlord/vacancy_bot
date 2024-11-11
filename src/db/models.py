from sqlalchemy import BigInteger, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class User(Base):
    __tablename__ = "users"

    id_user: Mapped[int] = mapped_column(BigInteger, unique=True)
    username: Mapped[str] = mapped_column(String(length=64), nullable=True)
    fullname: Mapped[str] = mapped_column(String(length=64), nullable=True)
    city: Mapped[str] = mapped_column(String(length=64), nullable=True)
    sub: Mapped[bool] = mapped_column(default=True)  # Подписка
    bot_blocked: Mapped[bool] = mapped_column(default=False)
    sub_active: Mapped[bool] = mapped_column(default=False)  # Активна ли подписка


class Sub(Base):
    __tablename__ = "subs"

    id_user: Mapped[int] = mapped_column(BigInteger)  # Идентификатор пользователя
    id_sub: Mapped[str] = mapped_column(String(length=12))  # Идентификатор подписки
    type_sub: Mapped[str] = mapped_column(String(length=12))  # Тип подписки
    sub_start_date: Mapped[str] = mapped_column(DateTime)  # Дата начала подписки
    sub_end_date: Mapped[str] = mapped_column(DateTime)  # Дата окончания подписки
    days: Mapped[int] = mapped_column()  # Количество дней подписки
    price: Mapped[int] = mapped_column()  # Стоимость подписки


class PostInfo(Base):
    __tablename__ = "posts_info"

    id_post: Mapped[str] = mapped_column(String(length=12))  # Идентификатор поста
    city: Mapped[str] = mapped_column(String(length=64))  # Город
    date_load: Mapped[str] = mapped_column(DateTime)  # Дата создания поста
    date_start_sending: Mapped[str] = mapped_column(
        DateTime
    )  # Дата начала отправки поста
    text: Mapped[str] = mapped_column(String(length=2048))
    photo_id: Mapped[str] = mapped_column(String(length=1000))
    is_sending_started: Mapped[bool] = mapped_column(
        default=False
    )  # Начата ли отправка поста
    is_sending_finished: Mapped[bool] = mapped_column(
        default=False
    )  # Отправлен ли пост всем


class PostMessage(Base):
    __tablename__ = "posts_message"

    id_post: Mapped[str] = mapped_column(String(length=12))  # Идентификатор поста
    id_user: Mapped[int] = mapped_column(BigInteger)  # Идентификатор пользователя
    id_message: Mapped[int] = mapped_column(BigInteger)  # Идентификатор сообщения


class Text(Base):
    __tablename__ = "texts"

    name: Mapped[str] = mapped_column(String(length=100))  # Название текста
    text: Mapped[str] = mapped_column(
        String(length=4096), default="текст не задан"
    )  # Текст


class Button(Base):
    __tablename__ = "buttons"

    name: Mapped[str] = mapped_column(String(length=100))  # Название кнопки
    text: Mapped[str] = mapped_column(
        String(length=64), default="кнопка"
    )  # Текст кнопки


class BlackList(Base):
    __tablename__ = "blacklist"

    id_user: Mapped[int] = mapped_column(BigInteger)  # Идентификатор пользователя


class Value(Base):
    __tablename__ = "values"

    name: Mapped[str] = mapped_column(String(length=100))  # Название значения
    value_int: Mapped[int] = mapped_column(BigInteger, default=0)  # Значение целое
    value_str: Mapped[str] = mapped_column(
        String(length=4096), default="не установлено"
    )  # Значение строка
