#(©)Codexbotz

import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait

from bot import Bot
from config import ADMINS, CHANNEL_ID, DISABLE_CHANNEL_BUTTON
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

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Get File", url=f'{shorty}')]])

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
    
    # Extract caption and file size
    caption = message.caption if message.caption else "No caption."
    file_size = message.file_size if message.file_size else "File size not available."
    
    # Create a "Get File" button
    get_file_button = InlineKeyboardButton("Get File", url=shorty)
    
    # Construct the message with the caption, file size, and the "Get File" button
    message_text = f"<b>Caption:</b>\n{caption}\n<b>File Size:</b> {file_size} bytes"
    
    # Create an inline keyboard with the "Get File" button
    reply_markup = InlineKeyboardMarkup([[get_file_button]])
    
    # Send the message with the button to the specified channel
    await client.send_message(-1001571229425, message_text, reply_markup=reply_markup, disable_web_page_preview=True)
    
    # Add the "Get File" button to the original message in the channel
    try:
        await message.edit_reply_markup(reply_markup)
    except Exception as e:
        print(e)
        pass



