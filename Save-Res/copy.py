from pyrogram import Client
import os
from dotenv import load_dotenv
from tqdm import tqdm
import time
import re
import sys

# from sqlite_db import links_force
from db_postgre import channel, jav_porn
from tools import tools

load_dotenv()
bot_token = os.getenv('TOKEN')
api_hash = os.getenv('API_HASH')
api_id = os.getenv('API_ID')

db = channel().get_all()
for i in db:
    print(f"{i.id} - {i.username} - {i.media_type}")

selected_id = input("Chose id....: ")
os.system('cls' if os.name == 'nt' else 'clear')
inf = channel.get_inf(id = int(selected_id))
user_name = inf.username
mess_id = inf.msgid
if inf.msgid_end is None or inf.msgid_end <= inf.msgid:
    print("End ID is not valid")
    sys.exit()
else:
    mess_end = inf.msgid_end
media_list = inf.media_type.upper().split(",")
target_id = inf.target_channel

Uncen = ["TAXD", "RKI", "259LUXU", "START", "MMUS", "MISM", "WAAA", "KKBT", "ADN", "200GANA", "NACR", "ATID", "SSIS", "IPX",
         "MIDE", "PRED", "ABW", "SSNI", "FSDSS", "DASS", "URE", "IPZZ", "HMN", "MIAB", "MIDV", "JUQ", "SONE", "GOOD", "HNDS",
         "CAWD", "MEYD", "MKMP", "ROE", "HMN", "CJOD", "MFK", "SDNM", "MSAJ", "SETM", "MTABS", "HBAD", "MOON", "DLDSS", "SAME",
         "KTB", "ABF", "300MIUM", "MIFD", "DPMI", "LULU", "NPJS", "CLUB", "GOJU", "FPRE", "336TNB", "ANKK", "NEOB", "FJIN",
         "KSBJ", "SDAM", "SGKI", "MIMK", "HZGD", "HSODA", "HDKA", "BBAN", "FOCS", "PPPE", "EBWH", "JUR"]

with Client("save_content_x_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token) as bot:
    chat = bot.get_chat(user_name)
    print(f"From: {user_name}\nTo: {target_id}\n\nIP: {tools.show_IP()}\n\nForwarding......")
    try:
        for i in tqdm(range(int(mess_id), int(mess_end)+1), desc = "....", unit="Post"):
            msg = bot.get_messages(user_name, i)

            # Lấy ra loại Media
            type_media = str(msg.media).replace('MessageMediaType.','').strip()

            caption = ""
            if type_media == 'VIDEO' and target_id != -1002069066600:
                caption = f"{msg.caption if msg.caption else ""}\n{(msg.video.file_name if msg.video.file_name else "")[:-4]} - {str(round(int(msg.video.file_size) / (1024 ** 3), 2))} GB"
            elif type_media == 'PHOTO' and target_id == -1002069066600:
                caption = msg.caption
            elif type_media == 'VIDEO' and target_id == -1002069066600:
                caption = msg.caption


            if type_media in media_list:
                try:
                    if 'fc2' in caption or 'FC2' in caption:
                        bot.copy_message(chat_id=-1001900564897, from_chat_id=chat.id, message_id=i, caption = caption)
                    elif re.search(r"\d{6}[_-]\d{2,3}", caption):
                        arry = re.findall(r"\d{6}[_-]\d{2,3}", caption)
                        for code in arry:
                            if jav_porn.check_exist(code) == False:
                                bot.copy_message(chat_id=-1002280926246, from_chat_id=chat.id, message_id=i, caption = caption)
                                break
                    elif "HEYZO" in caption.upper():
                        arry = re.findall(r"\d{4}", caption)
                        for code in arry:
                            if jav_porn.check_exist(code) == False:
                                bot.copy_message(chat_id=-1002280926246, from_chat_id=chat.id, message_id=i, caption = caption)
                                break
                    elif any(element in caption for element in Uncen):
                        bot.copy_message(chat_id=-1002398906809, from_chat_id=chat.id, message_id=i, caption = caption)
                    else:
                        bot.copy_message(chat_id=target_id, from_chat_id=chat.id, message_id=i, caption = caption)
                    print(f"\r{i} / {mess_end}  ", end='', flush=True)
                except Exception as e:
                    print(f"ERROR: {i}")
                links_force(username=user_name, msgid=i).update_links()
                time.sleep(3)
    except KeyboardInterrupt:
        print("\nEXIT")
