from pyrogram import Client
import os
from dotenv import load_dotenv
from tqdm import tqdm
import time
import re
import sys
from tools import tools

from save_to_txt import note
from postgree import jav_porn

load_dotenv()
bot_token = os.getenv('TOKEN')
api_hash = os.getenv('API_HASH')
api_id = os.getenv('API_ID')

print(note.get_all_user())
selected_id = input("Chose id....: ")
os.system('cls' if os.name == 'nt' else 'clear')
user_name, mess_id, mess_end, target_id, media = note.get_inf(int(selected_id))
media_list = media.upper().split(",")

if mess_id >= mess_end:
    print("msg_to is not valid")
    sys.exit()

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
                note.update_json(user_name,i)
                time.sleep(3)
    except KeyboardInterrupt:
        print("\nEXIT")
