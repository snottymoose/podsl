import asyncio
import os

from collections import defaultdict

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from dotenv import load_dotenv
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import LinkPreviewOptions


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

<a href="https://t.me/PODSLUSHKA_MLADA_BOSNA">@ПОДСЛУШКА</a> // <a href="http://t.me/mladabosnapodslushanbot">@БОТ</a> // <a href="https://t.me/MLADAB0SNA">@МЛАДА БОСНА🇧🇦</a>
"""


media_groups = defaultdict(list)


@dp.message()
async def handle_message(message: Message):

    if message.text == "/start":
        return

    user = message.from_user
    username = f"@{user.username}" if user.username else "-"


    if message.media_group_id:

        media_groups[message.media_group_id].append(message)

        await asyncio.sleep(1)

        messages = media_groups.pop(message.media_group_id, [])

        if not messages:
            return


        first = messages[0]

        if first.caption:
            text = (
                f"{first.caption}\n\n"
                f"{ADMIN_INFO.strip()}"
            )
        else:
            text = ADMIN_INFO.strip()


        await bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=text,
            link_preview_options=LinkPreviewOptions(is_disabled=True)
        )


        for msg in messages:

            if msg.photo:
                await bot.send_photo(
                    chat_id=ADMIN_CHAT_ID,
                    photo=msg.photo[-1].file_id
                )

            elif msg.video:
                await bot.send_video(
                    chat_id=ADMIN_CHAT_ID,
                    video=msg.video.file_id
                )

            elif msg.document:
                await bot.send_document(
                    chat_id=ADMIN_CHAT_ID,
                    document=msg.document.file_id
                )


    elif message.photo:

        if message.caption:
            text = (
                f"{message.caption}\n\n"
                f"{ADMIN_INFO.strip()}"
            )
        else:
            text = ADMIN_INFO.strip()


        await bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=text,
            link_preview_options=LinkPreviewOptions(is_disabled=True)
        )


        await bot.send_photo(
            chat_id=ADMIN_CHAT_ID,
            photo=message.photo[-1].file_id
        )


    elif message.document:

        if message.caption:
            text = (
                f"{message.caption}\n\n"
                f"{ADMIN_INFO.strip()}"
            )
        else:
            text = ADMIN_INFO.strip()

        await bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=text,
            link_preview_options=LinkPreviewOptions(is_disabled=True)
        )

        await bot.send_document(
            chat_id=ADMIN_CHAT_ID,
            document=message.document.file_id
        )

    elif message.document:

        await bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=ADMIN_INFO.strip(),
            link_preview_options=LinkPreviewOptions(is_disabled=True)
        )


        await bot.send_document(
            chat_id=ADMIN_CHAT_ID,
            document=message.document.file_id
        )


    elif message.text:

        await bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=(
                f"{message.text}\n\n"
                f"{ADMIN_INFO.strip()}"
            ),
            link_preview_options=LinkPreviewOptions(is_disabled=True)
        )

    await bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=(
            f"имя: {user.full_name}\n"
            f"юз: {username}\n"
            f"тг айди: <code>{user.id}</code>"
        )
    )


    await message.answer("ОТДАЙ ЮЗ")



async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())