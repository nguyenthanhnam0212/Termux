from pyrogram import Client
import os
from dotenv import load_dotenv
from tqdm import tqdm
import time

from tools import tools

load_dotenv()
bot_token = os.getenv('TOKEN')
api_hash = os.getenv('API_HASH')
api_id = os.getenv('API_ID')

os.system('cls' if os.name == 'nt' else 'clear')
user_name = "xhxstory"
mess_start = 4
mess_end = 1469
media_list = 'PHOTO'
target_id = "ai_x_img"

with Client("save_content_x_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token) as bot:
    chat = bot.get_chat(user_name)
    print(f"From: {user_name}\nTo: {target_id}\n\nIP: {tools.show_IP()}\n\nForwarding......")
    try:
        for i in tqdm(range(int(mess_start), int(mess_end)+1), desc = "....", unit="Post"):
            msg = bot.get_messages(user_name, i)

            # Lấy ra loại Media
            type_media = str(msg.media).replace('MessageMediaType.','').strip()

            if type_media in media_list:
                try:
                    # bot.copy_message(chat_id=target_id, from_chat_id=chat.id, message_id=i, caption = msg.caption)
                    bot.copy_message(chat_id=target_id, from_chat_id=chat.id, message_id=i, caption = '')
                    mess_start += 1
                    print(f"\r{i} / {mess_end}  ", end='', flush=True)
                except Exception as e:
                    print(f"msg_id = {mess_start}\nERROR: {i}")
                time.sleep(3)
    except KeyboardInterrupt:
        print("\nEXIT")
