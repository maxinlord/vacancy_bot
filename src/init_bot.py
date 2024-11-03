import config
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

bot: Bot = Bot(
    config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
