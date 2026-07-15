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
media_group_tasks = {}


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


    if message.media_group_id:

        group_id = message.media_group_id

        media_groups[group_id].append(message)


        if group_id in media_group_tasks:
            media_group_tasks[group_id].cancel()


        async def process_album():

            try:
                await asyncio.sleep(1)


                messages = media_groups.pop(group_id, [])


                if not messages:
                    return


                messages.sort(key=lambda x: x.message_id)


                first = next(
                    (m for m in messages if m.caption),
                    messages[0]
                )


                text = (
                    f"{first.caption}\n\n{ADMIN_INFO.strip()}"
                    if first.caption
                    else ADMIN_INFO.strip()
                )


                await send_admin_info(text)


                for msg in messages:

                    if msg.photo:
                        await bot.send_photo(
                            chat_id=ADMIN_CHAT_ID,
                            photo=msg.photo[-1].file_id
                        )


                await send_user_info(first.from_user)


                await first.answer("ОТДАЙ ЮЗ")


            finally:

                media_group_tasks.pop(group_id, None)



        media_group_tasks[group_id] = asyncio.create_task(
            process_album()
        )


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