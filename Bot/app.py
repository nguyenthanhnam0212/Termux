import asyncio
import re
from telebot.async_telebot import AsyncTeleBot
from telebot import types

from sqlite_db import temp_db

import os
from dotenv import load_dotenv
load_dotenv()

bot = AsyncTeleBot(os.getenv('TOKEN_DEV'))

val = {}
command = {}
array_media = []

@bot.message_handler(commands=['start'])
async def welcome(message):
    # await bot.set_chat_menu_button(message.chat.id,  menu_button=None)
    # await bot.delete_my_commands(scope=None, language_code=None)
    await bot.send_message(message.chat.id, '✅ STARTED', parse_mode="Markdown")
    command['status'] = 'start'

@bot.message_handler(commands=['gr'])
async def welcome(message):
    command['status'] = 'gr'
    var = temp_db().get_from_temp()
    if var != []:
        for i in var:
            if i.file_id_photo is not None:
                array_media.append(types.InputMediaPhoto(i.file_id_photo))
            if i.file_id_video is not None:
                array_media.append(types.InputMediaVideo(i.file_id_video))

        split_array_media= [array_media[i:i+9] for i in range(0, len(array_media), 9)]
        for j in split_array_media:
            await bot.send_media_group('-1002000065757', j)
        temp_db().truncate_temp()
        await bot.send_message(message.chat.id, "DONE")
    else:
        await bot.send_message(message.chat.id, "Forwad media to me !!!")
    array_media.clear()

@bot.message_handler(func=lambda message: True, content_types=['photo','video','text'])
async def handle_mess(message):
    match command['status']:
        case 'start':
            if message.video and 'id_channel' in val:
                match val['caption_type']:
                    case "file_c":
                        await bot.send_video(chat_id = val['id_channel'], video = message.video.file_id)
                    case "file_n":
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
                channel_id = re.search(r"[0-9]{12,13}", message.text)
                if channel_id and 'name' in message.text:
                    val['id_channel'] = f"-{channel_id[0]}"
                    val['caption_type'] = 'file_n'
                elif channel_id and 'name' not in message.text:
                    val['id_channel'] = f"-{channel_id[0]}"
                    val['caption_type'] = 'file_c'
                await bot.send_message(message.chat.id, f"Selected: `{val['id_channel']}`", parse_mode="Markdown")
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
