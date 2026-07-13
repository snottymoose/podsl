import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.types import Message, LinkPreviewOptions
from dotenv import load_dotenv
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = -1004313216807

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()

ADMIN_INFO = """
👍 - Ставлю «лосяру». 👍
👎 - Отдай юз

<a href="https://t.me/PODSLUSHKA_MLADA_BOSNA">@ПОДСЛУШКА</a> // <a href="https://t.me/mladabosnapodslushanbot">@БОТ</a> // <a href="https://t.me/MLADAB0SNA">@МЛАДА БОСНА🇧🇦</a>
"""


@dp.message()
async def handle_message(message: Message):
    user = message.from_user
    username = f"@{user.username}" if user.username else "-"

    # Берем текст сообщения (если его нет — выводим заглушку)
    user_text = message.text or "<не текстовое сообщение>"

    text = (
        f"{user_text}\n\n"
        f"{ADMIN_INFO}\n\n"
        f"👤 <b>имя:</b> {user.full_name}\n"
        f"🔗 <b>юз:</b> {username}\n"
        f"🆔 <b>тг айди:</b> <code>{user.id}</code>"
    )

    await bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=text,
        link_preview_options=LinkPreviewOptions(is_disabled=True)
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())