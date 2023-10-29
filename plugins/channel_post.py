#(©)Codexbotz

import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait

from bot import Bot
from config import ADMINS, CHANNEL_ID, DISABLE_CHANNEL_BUTTON, NEW_CAPTIONS_CHANNEL_ID
from helper_func import encode
from plugins.shorty import shorten_url, tiny

@Bot.on_message(filters.private & filters.user(ADMINS) & ~filters.command(['start','users','broadcast','batch','genlink','stats']))
async def channel_post(client: Client, message: Message):
    reply_text = await message.reply_text("Please Wait...!", quote = True)
    try:
        post_message = await message.copy(chat_id = client.db_channel.id, disable_notification=True)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        post_message = await message.copy(chat_id = client.db_channel.id, disable_notification=True)
    except Exception as e:
        print(e)
        await reply_text.edit_text("Something went Wrong..!")
        return
    converted_id = post_message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"
    shorty = tiny(shorten_url(link))

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔗 Get File", url=f'{shorty}')]])

    await reply_text.edit(f"<b>Here is your link</b>\n\n{shorty}", reply_markup=reply_markup, disable_web_page_preview = True)

    if not DISABLE_CHANNEL_BUTTON:
        await post_message.edit_reply_markup(reply_markup)

@Bot.on_message(filters.channel & filters.incoming & filters.chat(CHANNEL_ID))
async def new_post(client: Client, message: Message):

    if DISABLE_CHANNEL_BUTTON:
        return

    converted_id = message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"
    shorty = tiny(shorten_url(link))
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔗 Get File", url=f'{shorty}')]])
    try:
        await asyncio.sleep(15)
        
        await message.edit_reply_markup(reply_markup)

        caption = message.caption if message.caption else ""
        size = message.video 


        await client.send_message(
            NEW_CAPTIONS_CHANNEL_ID,
            f"<b>Join Backup Channel :- @BackupOfHighQualityRips\n\n<b>📂 Name: {caption}\n\n📦 Size: {humanbytes(size.file_size)}\n\n⌛️ Duration : {TimeFormatter(size.duration * 1000)}</b>", reply_markup=reply_markup, disable_web_page_preview = True
        )
    except Exception as e:
        print(e)
        pass

def humanbytes(size):
    # Function to format file size in a human-readable format
    if not size:
        return "0 B"
    # Define byte sizes
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    i = 0
    while size >= 1024 and i < len(suffixes) - 1:
        size /= 1024
        i += 1
    f = ('%.2f' % size).rstrip('0').rstrip('.')
    return f"{f} {suffixes[i]}"

def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + " days, ") if days else "") + \
        ((str(hours) + " hrs, ") if hours else "") + \
        ((str(minutes) + " min, ") if minutes else "") + \
        ((str(seconds) + " sec, ") if seconds else "") + \
        ((str(milliseconds) + " millisec, ") if milliseconds else "")
    return tmp[:-2]
