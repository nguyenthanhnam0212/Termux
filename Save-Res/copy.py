from pyrogram import Client
import os
from dotenv import load_dotenv
from tqdm import tqdm
import time

from sqlite_db import links_force

load_dotenv()

bot_token = os.getenv('TOKEN')
api_hash = os.getenv('API_HASH')
api_id = os.getenv('API_ID')

mess_end = os.getenv('MSG_ID')
user_name = os.getenv('USER_NAME')
inf = links_force(username=user_name).get_inf()
target_id = inf.target_channel
mess_id = inf.msgid

with Client("save_content_x_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token) as bot:

    def get_message_type(user_name, mess_id):
        msg = bot.get_messages(user_name, mess_id)
        type_media = str(msg.media)
        if 'PHOTO' in type_media:
            return 'Photo'
        elif 'VIDEO' in type_media:
            return 'Video'
        
    chat = bot.get_chat(user_name)
    print(f"From: {user_name}\nTo: {target_id}\n\nForwarding......")
    for i in tqdm(range(mess_id, int(mess_end) + 1), desc="Forwarding", unit="Post"):
        if get_message_type(user_name = user_name, mess_id = mess_id) in inf.media_type.split(","):
            try:
                bot.copy_message(chat_id=target_id, from_chat_id=chat.id, message_id=mess_id)
                print(f"\r{i} / {mess_end}  ", end='', flush=True)
            except Exception as e:
                print(f"\rERROR: {i} / {e}  ", end='', flush=True)
            links_force(username=os.getenv('USER_NAME'), msgid=i).update_links()
            time.sleep(3)