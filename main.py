import asyncio
import os

from collections import defaultdict

from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message,
    LinkPreviewOptions,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)
from aiogram.enums import ParseMode, ChatType
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
👎 - Я расист

<a href="https://t.me/AfterwakePODSLUSHANO">@ПОДСЛУШКА</a> // <a href="https://t.me/AfterwakePODSLUSHANO_bot">@БОТ</a> // <a href="https://t.me/afterwakesmp">@АФТЕРВЕЙК🌶🌶🌶</a>
"""


media_groups = defaultdict(list)
media_group_tasks = {}

admin_reply_to = {}


def reply_keyboard(user_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Ответить",
                    callback_data=f"reply:{user_id}"
                )
            ]
        ]
    )


async def send_admin_info(text, user_id=None):
    return await bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=text,
        link_preview_options=LinkPreviewOptions(is_disabled=True),
        reply_markup=reply_keyboard(user_id) if user_id else None
    )


async def send_user_info(user):
    return await bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=(
            f"имя: {user.full_name}\n"
            f"юз: {'@' + user.username if user.username else '-'}\n"
            f"тг айди: <code>{user.id}</code>"
        ),
        reply_markup=reply_keyboard(user.id)
    )


async def finish(message: Message):
    await send_user_info(message.from_user)
    await message.answer("ОТДАЙ ЮЗ")


@dp.callback_query(F.data.startswith("reply:"))
async def reply_callback(callback: CallbackQuery):

    if callback.message.chat.id != ADMIN_CHAT_ID:
        await callback.answer("нет доступа", show_alert=True)
        return

    user_id = int(callback.data.split(":")[1])

    admin_reply_to[callback.from_user.id] = user_id

    await callback.answer("пользователь выбран")

    await bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=(
            f"пиши ответ\n"
            f"отмена ответа: /cancel"
        )
    )


@dp.message(F.chat.id == ADMIN_CHAT_ID, F.text == "/cancel")
async def cancel_reply(message: Message):

    if message.from_user.id in admin_reply_to:
        del admin_reply_to[message.from_user.id]
        await message.answer("ответ отменен")
    else:
        await message.answer("нет ответа")


@dp.message(F.chat.id == ADMIN_CHAT_ID)
async def admin_message_handler(message: Message):

    admin_id = message.from_user.id

    if admin_id not in admin_reply_to:
        return

    user_id = admin_reply_to[admin_id]

    try:

        if message.text:
            await bot.send_message(
                chat_id=user_id,
            )

        elif message.photo:
            await bot.send_photo(
                chat_id=user_id,
                photo=message.photo[-1].file_id,
                caption=message.caption
            )

        elif message.video:
            await bot.send_video(
                chat_id=user_id,
                video=message.video.file_id,
                caption=message.caption
            )

        elif message.document:
            await bot.send_document(
                chat_id=user_id,
                document=message.document.file_id,
                caption=message.caption
            )

        else:
            await message.answer("тип сообщения не поддерживается")
            return

        await message.answer("отправлено")

        del admin_reply_to[admin_id]

    except Exception as e:

        await message.answer(
            f"не удалось отправить сообщение\n"
            f"<code>{e}</code>"
        )


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

                await send_admin_info(
                    text,
                    first.from_user.id
                )

                for msg in messages:

                    if msg.photo:
                        await bot.send_photo(
                            chat_id=ADMIN_CHAT_ID,
                            photo=msg.photo[-1].file_id,
                            reply_markup=reply_keyboard(
                                first.from_user.id
                            )
                        )

                    elif msg.video:
                        await bot.send_video(
                            chat_id=ADMIN_CHAT_ID,
                            video=msg.video.file_id,
                            reply_markup=reply_keyboard(
                                first.from_user.id
                            )
                        )

                    elif msg.document:
                        await bot.send_document(
                            chat_id=ADMIN_CHAT_ID,
                            document=msg.document.file_id,
                            reply_markup=reply_keyboard(
                                first.from_user.id
                            )
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
            caption=caption,
            reply_markup=reply_keyboard(message.from_user.id)
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
            caption=caption,
            reply_markup=reply_keyboard(message.from_user.id)
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
            caption=caption,
            reply_markup=reply_keyboard(message.from_user.id)
        )

        await finish(message)
        return


    if message.text:

        await bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=f"{message.text}\n\n{ADMIN_INFO.strip()}",
            link_preview_options=LinkPreviewOptions(is_disabled=True),
            reply_markup=reply_keyboard(message.from_user.id)
        )

        await finish(message)
        return


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
