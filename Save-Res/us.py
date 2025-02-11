from pyrogram import Client
import os
from dotenv import load_dotenv
from tqdm import tqdm
import time
import re
import sys

# from sqlite_db import links_force
from db_postgre import channel
from db_postgre_aiven import check
from tools import tools

load_dotenv()
bot_token = os.getenv('TOKEN')
api_hash = os.getenv('API_HASH')
api_id = os.getenv('API_ID')

os.system('cls' if os.name == 'nt' else 'clear')
inf = channel.get_inf(id = 13)
user_name = inf.username
mess_id = inf.msgid
if inf.msgid_end is None or inf.msgid_end <= inf.msgid:
    print("End ID is not valid")
    sys.exit()
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

            if type_media in media_list:
                try:
                    bot.copy_message(chat_id=target_id, from_chat_id=chat.id, message_id=i, caption = msg.caption)
                    print(f"\r{i} / {mess_end}  ", end='', flush=True)
                except Exception as e:
                    print(f"ERROR: {i}")
                channel(username=user_name, msgid=i).update_links()
                time.sleep(3)
    except KeyboardInterrupt:
        print("\nEXIT")
