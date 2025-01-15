from pyrogram import Client
import os
from dotenv import load_dotenv
from tqdm import tqdm
import time

from sqlite_db import links_force
from tools import tools

load_dotenv()
bot_token = os.getenv('TOKEN')
api_hash = os.getenv('API_HASH')
api_id = os.getenv('API_ID')

db = links_force().get_all_record()
for i in db:
    print(f"{i.id} - {i.username} - {i.media_type}")

selected_id = input("Chose id....: ")
os.system('cls' if os.name == 'nt' else 'clear')
inf = links_force.get_inf(id = selected_id)
user_name = inf.username
mess_id = inf.msgid
if inf.msgid_end is None or inf.msgid_end <= inf.msgid:
    mess_end = mess_id + 100
else:
    mess_end = inf.msgid_end
media_list = inf.media_type.upper().split(",")
target_id = inf.target_channel

with Client("save_content_x_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token) as bot:
    chat = bot.get_chat(user_name)
    print(f"From: {user_name}\nTo: {target_id}\n\nIP: {tools.show_IP()}\n\nForwarding......")
    try:
        for i in tqdm(range(int(mess_id), int(mess_end)+1), desc = "....", unit="Post"):
            msg = bot.get_messages(user_name, i)

            # Lấy ra loại Media
            type_media = str(msg.media).replace('MessageMediaType.','').strip()

            caption = ""
            if type_media == 'VIDEO':
                caption = f"{msg.caption if msg.caption else ""}\n{(msg.video.file_name if msg.video.file_name else "")[:-4]} - {str(round(int(msg.video.file_size) / (1024 ** 3), 2))} GB"

            if type_media in media_list:
                try:
                    if 'fc2' in caption or 'FC2' in caption:
                        bot.copy_message(chat_id=-1001900564897, from_chat_id=chat.id, message_id=i, caption = caption)
                    else:
                        bot.copy_message(chat_id=target_id, from_chat_id=chat.id, message_id=i, caption = caption)
                    print(f"\r{i} / {mess_end}  ", end='', flush=True)
                except Exception as e:
                    print(f"ERROR: {i}")
                links_force(username=user_name, msgid=i).update_links()
                time.sleep(3)
    except KeyboardInterrupt:
        print("\nEXIT")
