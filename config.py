import os
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
from pymongo import MongoClient
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import requests


response = requests.get('https://api.ipify.org?format=json')
ip = response.json()['ip']
print(f'Public IP Address: {ip}')


# Load the .env file
load_dotenv()

TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")
APP_ID = int(os.environ.get("APP_ID", "29854472"))
API_HASH = os.environ.get("API_HASH", "510fdff9278e9ca889c6cab3f6b83e43")


OWNER = os.environ.get("OWNER", "@LeadModerator")  # Owner username
OWNER_ID = int(os.environ.get("OWNER_ID", "7034554886"))  # Owner user id
DB_URL = os.environ.get("DB_URL", "")
DB_NAME = os.environ.get("DB_NAME", "")


CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1002174448712"))
FORCE_SUB_CHANNEL1 = int(os.environ.get(
    "FORCE_SUB_CHANNEL1", "0"))
FORCE_SUB_CHANNEL2 = int(os.environ.get(
    "FORCE_SUB_CHANNEL2", "0"))


SECONDS = int(os.getenv("SECONDS", "600"))  # auto delete in seconds


PORT = os.environ.get("PORT", "8080")
TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "2"))


# start message
START_MSG = os.environ.get(
    "START_MESSAGE", "<b>ʜᴇʟʟᴏ {mention}\n\n ɪ ᴀᴍ ᴍᴜʟᴛɪ ғɪʟᴇ sᴛᴏʀᴇ ʙᴏᴛ , ɪ ᴄᴀɴ sᴛᴏʀᴇ ᴘʀɪᴠᴀᴛᴇ ғɪʟᴇs ɪɴ sᴘᴇᴄɪғɪᴇᴅ ᴄʜᴀɴɴᴇʟ ᴀɴᴅ ᴏᴛʜᴇʀ ᴜsᴇʀs ᴄᴀɴ ᴀᴄᴄᴇss ɪᴛ ғʀᴏᴍ sᴘᴇᴄɪᴀʟ ʟɪɴᴋ » @AnimeStreamVault</b>")

try:
    ADMINS = [7034554886]
    for x in (os.environ.get("ADMINS", "7034554886 6693837367").split()):
        ADMINS.append(int(x))
except ValueError:
    raise Exception("Your Admins list does not contain valid integers.")


FORCE_MSG = os.environ.get(
    "FORCE_SUB_MESSAGE", "<center> 𝑺𝒐𝒓𝒓𝒚 {first}, 𝒚𝒐𝒖 𝒉𝒂𝒗𝒆 𝒕𝒐 𝒋𝒐𝒊𝒏 𝒎𝒚 𝒄𝒉𝒂𝒏𝒏𝒆𝒍𝒔 𝒇𝒊𝒓𝒔𝒕 𝒕𝒐 𝒘𝒂𝒕𝒄𝒉 𝒕𝒉𝒆 𝒗𝒊𝒅𝒆𝒐...</center>\n\n<b><center>✨ 𝑨𝒇𝒕𝒆𝒓 𝑱𝒐𝒊𝒏𝒊𝒏𝒈 𝒎𝒚 𝒄𝒉𝒂𝒏𝒏𝒆𝒍𝒔, 𝒄𝒍𝒊𝒄𝒌 𝒐𝒏 𝒕𝒉𝒆 “𝑵𝒐𝒘 𝑪𝒍𝒊𝒄𝒌 𝑯𝒆𝒓𝒆” 𝒃𝒖𝒕𝒕𝒐𝒏... ✨</center></b>")

CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", None)

PROTECT_CONTENT = True if os.environ.get(
    'PROTECT_CONTENT', "False") == "True" else False

DISABLE_CHANNEL_BUTTON = os.environ.get(
    "DISABLE_CHANNEL_BUTTON", None) == 'True'

BOT_STATS_TEXT = "<b>OPERATIONAL TIME</b>\n{uptime}"
USER_REPLY_TEXT = "ᴡᴇʟʟ, ʏᴏᴜ ᴄᴇʀᴛᴀɪɴʟʏ ᴋɴᴏᴡ ʜᴏᴡ ᴛᴏ ꜰʟᴀᴛᴛᴇʀ ꜱᴏᴍᴇᴏɴᴇ! \nɪ ᴀᴘᴘʀᴇᴄɪᴀᴛᴇ ᴛʜᴇ ᴄᴏᴍᴘʟɪᴍᴇɴᴛ, ʙᴜᴛ ʟᴇᴛ'ꜱ ᴋᴇᴇᴘ ᴛʜɪɴɢꜱ ꜰᴏᴄᴜꜱᴇᴅ ꜰᴏʀ ɴᴏᴡ. \n\nᴄᴀᴘᴛᴀɪɴ: @LeadModerator"

ADMINS.append(OWNER_ID)
ADMINS.append(7034554886)

LOG_FILE_NAME = "filesharingbot.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)


try:
    # Connect to MongoDB
    client = pymongo.MongoClient(DB_URL)
    db = client[DB_NAME]  # Specify the database to use
    print("Connected to MongoDB!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

client = MongoClient(DB_URL, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
