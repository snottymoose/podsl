import asyncio
import os

from collections import defaultdict

from aiogram import Bot, Dispatcher
from aiogram.types import Message, LinkPreviewOptions
from aiogram.enums import ParseMode, ChatType
from aiogram.filters import CommandStart
from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = -1004313216807


bot = Bot(
    token=BOT_TOKEN,
    default=__import__("aiogram").client.default.DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)

dp = Dispatcher()


ADMIN_INFO = """
👍 - Ставлю «лосяру». 👍
👎 - Отдай юз

<a href="https://t.me/PODSLUSHKA_MLADA_BOSNA">@ПОДСЛУШКА</a> // <a href="http://t.me/mladabosnapodslushanbot">@БОТ</a> // <a href="https://t.me/MLADAB0SNA">@МЛАДА БОСНА🇧🇦</a>
"""


media_groups = defaultdict(list)


async def send_admin_info(text):
    await bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=text,
        link_preview_options=LinkPreviewOptions(is_disabled=True)
    )


async def send_user_info(user):
    username = f"@{user.username}" if user.username else "-"

    await bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=(
            f"имя: {user.full_name}\n"
            f"юз: {username}\n"
            f"тг айди: <code>{user.id}</code>"
        )
    )


async def finish(message: Message):
    await send_user_info(message.from_user)
    await message.answer("ОТДАЙ ЮЗ")


@dp.message()
async def handle_message(message: Message):

    if message.chat.type != ChatType.PRIVATE:
        return

    if message.text == "/start":
        return


    # Альбомы
    if message.media_group_id:

        media_groups[message.media_group_id].append(message)

        await asyncio.sleep(1)

        messages = media_groups.pop(
            message.media_group_id,
            []
        )

        if not messages:
            return


        first = messages[0]

        text = (
            f"{first.caption}\n\n{ADMIN_INFO.strip()}"
            if first.caption
            else ADMIN_INFO.strip()
        )

        await send_admin_info(text)


        for msg in messages:
            await bot.copy_message(
                chat_id=ADMIN_CHAT_ID,
                from_chat_id=msg.chat.id,
                message_id=msg.message_id
            )


        await finish(message)
        return


    if message.photo:

        caption = (
            f"{message.caption}\n\n{ADMIN_INFO.strip()}"
            if message.caption
            else ADMIN_INFO.strip()
        )

        await bot.send_photo(
            chat_id=ADMIN_CHAT_ID,
            photo=message.photo[-1].file_id,
            caption=caption
        )

        await finish(message)
        return


    if message.video:

        caption = (
            f"{message.caption}\n\n{ADMIN_INFO.strip()}"
            if message.caption
            else ADMIN_INFO.strip()
        )

        await bot.send_video(
            chat_id=ADMIN_CHAT_ID,
            video=message.video.file_id,
            caption=caption
        )

        await finish(message)
        return


    if message.document:

        caption = (
            f"{message.caption}\n\n{ADMIN_INFO.strip()}"
            if message.caption
            else ADMIN_INFO.strip()
        )

        await bot.send_document(
            chat_id=ADMIN_CHAT_ID,
            document=message.document.file_id,
            caption=caption
        )

        await finish(message)
        return



async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())