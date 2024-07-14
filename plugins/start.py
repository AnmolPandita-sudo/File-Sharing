from config import ADMINS, OWNER_ID
from pyrogram.types import Message
from pyrogram import Client, filters
import os
import asyncio
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
from bot import Bot
from config import ADMINS, FORCE_MSG, START_MSG, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, PROTECT_CONTENT
from helper_func import subscribed, decode, get_messages
from database.database import add_user, present_user, del_user, full_userbase, user_data
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from io import BytesIO

# Add time in seconds for waiting before deleting
SECONDS = int(os.getenv("SECONDS", "600"))


#
##
###
####
#####
######
#######
######## ---------------           START COMMAND WITH OR WITHOUT LINK            ---------------########
#######
######
#####
####
###
##
#


@Bot.on_message(filters.command('start') & filters.private & subscribed)
async def start_command(client: Client, message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name  # Access last name

    # Add user to database if not present
    if not await present_user(user_id, username, first_name, last_name):
        try:
            await add_user(user_id, username, first_name, last_name)
        except Exception as e:
            print(f"Error adding user: {e}")

    text = message.text

    text = message.text

    if len(text) > 7:
        try:
            base64_string = text.split(" ", 1)[1]
            string = await decode(base64_string)
            argument = string.split("-")

            if len(argument) == 3:
                try:
                    start = int(int(argument[1]) / abs(client.db_channel.id))
                    end = int(int(argument[2]) / abs(client.db_channel.id))
                    ids = range(start, end + 1) if start <= end else []

                except Exception as e:
                    print(f"Error parsing argument: {e}")
                    return

            elif len(argument) == 2:
                try:
                    ids = [int(int(argument[1]) / abs(client.db_channel.id))]

                except Exception as e:
                    print(f"Error parsing argument: {e}")
                    return

            else:
                return

        except Exception as e:
            print(f"Error decoding argument: {e}")
            return

    else:
        #####
        ######
        #######
        ######## ---------------           START COMMAND WITHOUT LINK            ---------------########
        #######
        ######
        #####
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "⚡️🇦​​​​​🇧​​​​​🇴​​​​​🇺​​​​​🇹​​​​​ 🇲​​​​​🇪​​​​⚡️", callback_data="about"),
                    InlineKeyboardButton(
                        "❌ 🇨​​​​​🇱​​​​​🇴​​​​​🇸​​​​​🇪​​​​ ❌ ", callback_data="close")
                ]
            ]
        )
        await message.reply_text(
            text=START_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username=None if not message.from_user.username else '@' + message.from_user.username,
                mention=message.from_user.mention,
                id=message.from_user.id
            ),
            reply_markup=reply_markup,
            disable_web_page_preview=True,
            quote=True
        )
        return

    #####
    ######
    #######
    ######## ---------------           START COMMAND WITH LINK            ---------------########
    #######
    ######
    #####
    temp_msg = await message.reply("!! ᴄᴏɴᴛᴇɴᴛ ᴠᴇᴛᴛɪɴɢ !!")

    try:
        messages = await get_messages(client, ids)

    except Exception as e:
        print(f"Error fetching messages: {e}")
        await temp_msg.edit_text("ᴇʀʀᴏʀ ꜰᴇᴛᴄʜɪɴɢ ᴄᴏɴᴛᴇɴᴛ. ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ.")
        return

    if not messages:
        sent_msg = await message.reply_text("ɴɪɢɢᴀ ʏᴏᴜ ʟᴀᴛᴇ. ɢᴇᴛ ʏᴏᴜʀ ᴀss ɪɴ ʜᴇʀᴇ ɪɴ ᴛɪᴍᴇ")

        # Auto delete the message after 7 seconds
        await asyncio.sleep(10)
        try:
            await sent_msg.delete()
        except Exception as e:
            print(f"Error deleting message: {e}")

        return

    # Wait for 3 seconds before sending files
    await asyncio.sleep(3)
    await temp_msg.edit_text("!!!!   ꜱᴇɴᴅɪɴɢ ꜰɪʟᴇꜱ   !!!!")
    await asyncio.sleep(1)

    # Check if temp_msg still exists before deleting
    if temp_msg:
        await temp_msg.delete()

    sent_messages = []
    found_files = False

    for msg in messages:
        # Check if the message is empty (no document)
        if msg.document is None:
            # Skip empty files
            continue

        found_files = True

        # Generate caption based on configuration
        if bool(CUSTOM_CAPTION) and bool(msg.document):
            caption = CUSTOM_CAPTION.format(
                previouscaption="" if not msg.caption else msg.caption.html,
                filename=msg.document.file_name
            )
        else:
            caption = "" if not msg.caption else msg.caption.html

        # Determine reply markup based on configuration
        if DISABLE_CHANNEL_BUTTON:
            reply_markup = msg.reply_markup
        else:
            reply_markup = None

        try:
            # Copy message to user with specified settings
            copied_msg = await msg.copy(
                chat_id=message.from_user.id,
                caption=caption,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup,
                protect_content=PROTECT_CONTENT
            )
            sent_messages.append(copied_msg)

        except FloodWait as e:
            await asyncio.sleep(e.x)
            copied_msg = await msg.copy(
                chat_id=message.from_user.id,
                caption=caption,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup,
                protect_content=PROTECT_CONTENT
            )
            sent_messages.append(copied_msg)

        except:
            pass

    if found_files:
        # Notify the user about the deletion process and wait before deletion
        deletion_msg = await client.send_message(
            chat_id=message.from_user.id,
            text="<b>❗️ <u>ᴜʀɢᴇɴᴛ</u> ❗️</b>\n\nʏᴏ, ʟɪsᴛᴇɴ ᴜᴘ! ᴛʜɪs ᴇᴘɪsᴏᴅᴇ / ꜰɪʟᴇ ɪs ᴏɴ ᴛʜᴇ ᴄʜᴏᴘᴘɪɴɢ ʙʟᴏᴄᴋ, sᴇᴛ ᴛᴏ ᴠᴀɴɪsʜ ɪɴ 10 ᴍɪɴᴜᴛᴇs (ᴛʜᴀɴᴋs ᴛᴏ ᴘᴇsᴋʏ ᴄᴏᴘʏʀɪɢʜᴛ ɪssᴜᴇs).\n\n📌 ʜᴜʀʀʏ ᴀɴᴅ sᴘʀᴇᴀᴅ ɪᴛ ᴛᴏ ᴀɴᴏᴛʜᴇʀ ᴘʟᴀᴄᴇ, sᴛᴀʀᴛ ᴛʜᴇ ᴅᴏᴡɴʟᴏᴀᴅ ᴀsᴀᴘ!",
            parse_mode=ParseMode.HTML
        )

        await asyncio.sleep(SECONDS)

        # Delete each sent message and update the user
        for msg in sent_messages:
            try:
                await msg.delete()

            except Exception as e:
                print(f"Error deleting message: {e}")
                pass

        # Inform user about completion of deletion process
        await deletion_msg.edit_text("Nᴀɴɪ???😨😧 \nMʏ ᴀɴɪᴍᴇ ᴄᴏʟʟᴇᴄᴛɪᴏɴ? ᴅᴜsᴛ! Dᴀᴛᴀ ɢʀᴇᴍʟɪɴs, ᴛʜɪs ɪs ᴀ sʜᴀʀɪɴɢᴀɴ-ʟᴇᴠᴇʟ ᴏꜰꜰᴇɴsᴇ! \n\nOɴᴇ ʀᴇϙᴜᴇsᴛ, ᴀɴᴅ ᴍʏ ʙᴀɴᴋᴀɪ ᴏꜰ ᴠᴇɴɢᴇᴀɴᴄᴇ ʀᴇsᴛᴏʀᴇs ᴡᴀɪꜰᴜs ᴀɴᴅ ʙᴀᴛᴛʟᴇs! Yᴏᴜ ᴡɪʟʟ ʀᴇɢʀᴇᴛ ᴛʜɪs!   🔥💪")

    else:
        # No files found, inform the user
        sent_msg = await message.reply_text("ɴɪɢɢᴀ ʏᴏᴜ ʟᴀᴛᴇ. ɢᴇᴛ ʏᴏᴜʀ ᴀss ɪɴ ʜᴇʀᴇ ɪɴ ᴛɪᴍᴇ")

        # Auto delete the message after 7 seconds
        await asyncio.sleep(7)
        try:
            await sent_msg.delete()
        except Exception as e:
            print(f"Error deleting message: {e}")
    return


# =====================================================================================##
# =====================================================================================##
# =====================================================================================##
# =====================================================================================##
# =====================================================================================##

WAIT_MSG = """"<b>Processing ...</b>"""

REPLY_ERROR = """<code>Use this command as a replay to any telegram message without any spaces.</code>"""

# =====================================================================================##
# =====================================================================================##
# =====================================================================================##
# =====================================================================================##
# =====================================================================================##


@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client, message: Message):
    buttons = [
        [
            InlineKeyboardButton(text="• ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url=client.invitelink),
            InlineKeyboardButton(text="ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ •",
                                 url=client.invitelink2),
        ]
    ]

    try:
        url = f"https://t.me/{client.username}?start={message.command[1]}"
        buttons.append(
            [
                InlineKeyboardButton(
                    text='• ɴᴏᴡ ᴄʟɪᴄᴋ ʜᴇʀᴇ •',
                    url=url
                )
            ]
        )
    except IndexError:
        pass

    await message.reply(
        text=FORCE_MSG.format(
            first=message.from_user.first_name,
            last=message.from_user.last_name,
            username=None if not message.from_user.username else '@' + message.from_user.username,
            mention=message.from_user.mention,
            id=message.from_user.id
        ),
        reply_markup=InlineKeyboardMarkup(buttons),
        quote=True,
        disable_web_page_preview=True
    )

#
##
###
####
#####
######
#######
######## ---------------            USERS USING BOT COMMAND            ---------------########
#######
######
#####
####
###
##
#


@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    try:
        # Sending initial message
        msg = await client.send_message(chat_id=message.chat.id, text="Fetching user data...")

        # Fetch user data
        users = await full_userbase()
        num_users = len(users)

        # Prepare PDF content
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()

        elements = []

       # Centered heading 1
        heading_text = f"{num_users} USERS ARE USING THE BOT"
        centered_heading = Paragraph(heading_text, styles['Heading1'])
        centered_heading.alignment = 1  # 0=left, 1=center, 2=right
        elements.append(centered_heading)

        # Centered heading 2
        centered_heading2 = Paragraph("USER DATA : ", styles['Heading2'])
        centered_heading2.alignment = 1  # 0=left, 1=center, 2=right
        elements.append(centered_heading2)
        elements.append(Spacer(1, 6))

        # Prepare table data
        data = [['USER ID', 'USERNAME', 'FIRST  NAME', 'LAST  NAME']]
        for user in users:
            data.append([user['_id'], user.get('username', ''), user.get(
                'first_name', ''), user.get('last_name', '')])

        # Build table
        table_style = [('GRID', (0, 0), (-1, -1), 2, (0, 0, 0)),
                       ('BACKGROUND', (0, 0), (-1, -1), (240/255, 240/255, 240/255))]
        tbl = Table(data, style=table_style)
        elements.append(tbl)

        # Build PDF document
        doc.build(elements)

        # Save PDF to a file
        pdf_file = "User_Data.pdf"
        with open(pdf_file, "wb") as file:
            file.write(buffer.getvalue())

        # Send message with user count and send the PDF file
        await msg.edit(f"{num_users} ᴜꜱᴇʀꜱ ᴀʀᴇ ᴜꜱɪɴɢ ᴛʜɪꜱ ʙᴏᴛ.")

        # Send the PDF file as a document
        sent_message = await client.send_document(chat_id=message.chat.id, document=pdf_file, caption="ʜᴇʀᴇ ɪꜱ ᴛʜᴇ ᴜꜱᴇʀ ᴅᴀᴛᴀ.")

        # Auto delete the sent PDF message and PDF file from the system after 10 seconds
        await asyncio.sleep(10)
        try:
            await sent_message.delete()
            os.remove(pdf_file)
        except Exception as e:
            print(f"Error deleting message: {e}")

    except Exception as e:
        print(f"Error fetching or sending user data: {e}")

#
##
###
####
#####
######
#######
######## ---------------            BROADCAST COMMAND(with BUTTONS)            ---------------########
#######
######
#####
####
###
##
#


@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    if message.reply_to_message:
        try:
            user_docs = await full_userbase()
            user_ids = [user['_id']
                        for user in user_docs if user['_id'] != OWNER_ID]
            broadcast_msg = message.reply_to_message
            total = 0
            successful = 0
            blocked = 0
            deleted = 0
            unsuccessful = 0

            pls_wait = await message.reply("<i>Broadcasting Message.. This will Take Some Time</i>")
            for user_id in user_ids:
                try:
                    await broadcast_msg.copy(user_id)
                    successful += 1
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    await broadcast_msg.copy(user_id)
                    successful += 1
                except UserIsBlocked:
                    await del_user(user_id)
                    blocked += 1
                except InputUserDeactivated:
                    await del_user(user_id)
                    deleted += 1
                except:
                    unsuccessful += 1
                    pass
                total += 1

            status = f"""<b><u>Broadcast Completed</u>

    Total Users: <code>{total}</code>
    Successful: <code>{successful}</code>
    Blocked Users: <code>{blocked}</code>
    Deleted Accounts: <code>{deleted}</code>
    Unsuccessful: <code>{unsuccessful}</code></b>"""

            await pls_wait.edit(status)
        except:
            pass

    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()
