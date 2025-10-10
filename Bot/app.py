import asyncio
import re
from telebot.async_telebot import AsyncTeleBot
from telebot import types

from db_sqlite import temp_db

import os
from dotenv import load_dotenv
load_dotenv()

bot = AsyncTeleBot(os.getenv('TOKEN_DEV'))

g_val = {
    "channel_id": "-1002000065757",
    "caption_type": "name",
    "command": None
}
array_media = []

@bot.message_handler(commands=['start'])
async def welcome(message):
    await bot.set_chat_menu_button(message.chat.id,  menu_button=None)
    await bot.delete_my_commands(scope=None, language_code=None)
    await bot.send_message(message.chat.id, '❤️', parse_mode="Markdown")
    g_val['command'] = 'start'

@bot.message_handler(commands=['gr'])
async def welcome(message):
    g_val['command'] = 'gr'
    var = temp_db().get_from_temp()
    if var != []:
        for i in var:
            if i.file_id_photo is not None:
                array_media.append(types.InputMediaPhoto(i.file_id_photo))
            if i.file_id_video is not None:
                array_media.append(types.InputMediaVideo(i.file_id_video))

        split_array_media= [array_media[i:i+9] for i in range(0, len(array_media), 9)]
        for j in split_array_media:
            await bot.send_media_group(g_val['channel_id'], j)
        temp_db().truncate_temp()
        await bot.send_message(message.chat.id, "DONE")
    else:
        await bot.send_message(message.chat.id, "Forwad media to me !!!")
    array_media.clear()

@bot.message_handler(func=lambda message: True, content_types=['photo','video','text'])
async def handle_mess(message):
    if message.text:
        if re.search(r"[0-9]{12,13}", message.text):
            g_val['channel_id'] = message.text
        await bot.send_message(message.chat.id, f"Selected: `{g_val['channel_id']}`", parse_mode="Markdown")
    match g_val['command']:
        case 'start':
            if message.video :
                try:
                    file_name = (message.video.file_name)[:-4]
                    file_caption = message.caption
                    cap = f"{file_caption}\n{file_name}"
                except:
                    cap = message.caption
                await bot.send_video(chat_id = g_val['channel_id'], video = message.video.file_id, caption = cap)
                await bot.delete_message(message.chat.id, message.id)
            elif message.photo:
                await bot.send_photo(chat_id = g_val['channel_id'], photo = message.photo[-1].file_id)
                await bot.delete_message(message.chat.id, message.id)
    
        case 'gr':
            if message.photo:
                try:
                    temp_db(file_id_photo = message.photo[-1].file_id).save_to_temp()
                    await bot.delete_message(message.chat.id, message.id)
                except:
                    await bot.send_message(message.chat.id, "INSERT FAIL")
                    temp_db.reset()
            elif message.video:
                try:
                    temp_db(file_id_video = message.video.file_id, file_size = message.video.file_size, video_duration = message.video.duration).save_to_temp()
                    await bot.delete_message(message.chat.id, message.id)
                except:
                    await bot.send_message(message.chat.id, "INSERT FAIL")
                    temp_db.reset()

asyncio.run(bot.polling())
