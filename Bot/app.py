import asyncio
import re
from telebot.async_telebot import AsyncTeleBot

import os
from dotenv import load_dotenv
load_dotenv("env/.env")

bot = AsyncTeleBot(os.getenv('TOKEN_DEV'))

val = {}

@bot.message_handler(commands=['start'])
async def welcome(message):
    # await bot.set_chat_menu_button(message.chat.id,  menu_button=None)
    # await bot.delete_my_commands(scope=None, language_code=None)
    await bot.send_message(message.chat.id, 'Bot Đang Hoạt Động ... ', parse_mode="Markdown")
@bot.message_handler(func=lambda message: True, content_types=['photo','video','text'])
async def handle_forward(message):
    if message.video and 'id_channel' in val:
        cap = message.video.file_name
        if cap is not None:
            cap = f"{cap[:-4]}"
        else:
            cap = message.caption
        await bot.send_video(chat_id = val['id_channel'], video = message.video.file_id, caption = cap)
        await bot.delete_message(message.chat.id, message.id)
    elif message.photo and 'id_channel' in val:
        await bot.send_photo(chat_id = val['id_channel'], photo = message.photo[-1].file_id)
        await bot.delete_message(message.chat.id, message.id)
    elif message.text:
        if re.search(r"[0-9]{12,13}", message.text):
            val['id_channel'] = message.text
            await bot.send_message(message.chat.id, f"Selected: {val['id_channel']}")

asyncio.run(bot.polling())
