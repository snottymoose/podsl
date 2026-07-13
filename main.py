import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from dotenv import load_dotenv
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import LinkPreviewOptions

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT"))

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()

ADMIN_INFO = """
👍 - Ставлю «лосяру». 👍
👎 - Отдай юз

<a href="https://t.me/PODSLUSHKA_MLADA_BOSNA">@ПОДСЛУШКА</a> // <a href="http://t.me/mladabosnapodslushanbot">@БОТ</a> // <a href="https://t.me/MLADAB0SNA">@МЛАДА БОСНА🇧🇦</a>
"""


@dp.message()
async def handle_message(message: Message):

    await bot.forward_message(
        chat_id=ADMIN_CHAT_ID,
        from_chat_id=message.chat.id,
        message_id=message.message_id,
    )

    await bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=ADMIN_INFO,
        link_preview_options=LinkPreviewOptions(is_disabled=True)
    )

    user = message.from_user

    username = (
        f"@{user.username}"
        if user.username
        else "-"
    )

    await bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=(
            f"имя: {user.full_name}\n"
            f"юз: {username}\n"
            f"тг айди: <code>{user.id}</code>"
        )
    )