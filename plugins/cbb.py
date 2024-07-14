from pyrogram import __version__
from bot import Bot
from config import OWNER_ID
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery


@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    message = query.message  # Store query.message in a variable for easier access
    if not message:
        print("Error: query.message is None")
        return

    if data == "about":
        await message.edit_text(
            text=f"""<b>🤖 My Name :</b> <a href='https://t.me/FileSharingXProBot'>File Sharing Bot</a>
                     <b>📝 Language :</b> <a href='https://python.org'>Python 3</a>
                     <b>📚 Library :</b> <a href='https://pyrogram.org'>Pyrogram {__version__}</a>
                     <b>🚀 Server :</b> <a href='https://app.koyeb.com/'>Koyeb</a>
                     <b>📢 Channel :</b> <a href='https://t.me/DarkHumorHub'>Dark Humor Hub</a>
                     <b>🧑‍💻 Developer :</b> <a href='tg://user?id={OWNER_ID}'>Admin</a>""",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "❌ 🇨​​​​​🇱​​​​​🇴​​​​​🇸​​​​​🇪​​​​ ❌", callback_data="close")
                    ]
                ]
            )
        )
    elif data == "close":
        try:
            await message.delete()
            if message.reply_to_message:
                await message.reply_to_message.delete()
        except Exception as e:
            print(f"Error deleting message: {e}")
