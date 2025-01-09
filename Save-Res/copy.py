import pyrogram
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant, InviteHashExpired, UsernameNotOccupied

import time
import os
import threading

from postgree import links_force
from tqdm import tqdm

import os
from dotenv import load_dotenv
load_dotenv()

bot_token = os.getenv('TOKEN')
api_hash = os.getenv('API_HASH')
api_id = os.getenv('API_ID')
bot = Client("save_content_x_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# ss = os.getenv('SESSION')
ss = None
if ss is not None:
	acc = Client("auto_telegram_0212" ,api_id=api_id, api_hash=api_hash, session_string=ss)
	acc.start()
else: 
	acc = None


# start command
@bot.on_message(filters.command(["start"]))
def save(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
	# message.delete()

	mess = message.text
	arr_mess = mess.split(":")
	uss = arr_mess[0].strip()
	to_id = int(arr_mess[1].strip())+1
	inf = links_force(username=uss).get_inf()
	type_media = inf.media_type.split(",")
	from_id = inf.msgid
	target_id = inf.target_channel
	print(f"From: {uss}\nTo: {target_id}\n\nForwarding......")
	for i in tqdm(range(from_id, to_id), desc="Forwarding", unit="Post"):
		message.text = f"https://t.me/{uss}/{i}"
		print(f"\r{i} / {to_id-1}  ", end='', flush=True)
		# joining chats
		if "https://t.me/+" in message.text or "https://t.me/joinchat/" in message.text:

			if acc is None:
				bot.send_message(message.chat.id,f"**String Session is not Set**")
				return

			try:
				try: acc.join_chat(message.text)
				except Exception as e: 
					bot.send_message(message.chat.id,f"**Error** : __{e}__")
					return
				bot.send_message(message.chat.id,"**Chat Joined**")
			except UserAlreadyParticipant:
				bot.send_message(message.chat.id,"**Chat alredy Joined**")
			except InviteHashExpired:
				bot.send_message(message.chat.id,"**Invalid Link**")

		# getting message
		elif "https://t.me/" in message.text:

			datas = message.text.split("/")
			temp = datas[-1].replace("?single","").split("-")
			fromID = int(temp[0].strip())
			try: toID = int(temp[1].strip())
			except: toID = fromID

			for msgid in range(fromID, toID+1):
				username = datas[3]

				try: msg  = bot.get_messages(username,msgid)
				except UsernameNotOccupied: 
					bot.send_message(message.chat.id,f"**The username is not occupied by anyone**")
					return
				if get_message_type(msg) in type_media:
					try:
						if '?single' not in message.text:
							bot.copy_message(target_id, msg.chat.id, msg.id)
							# bot.copy_message(message.chat.id, msg.chat.id, msg.id)
						else:
							bot.copy_media_group(-1001723907536, msg.chat.id, msg.id)
							# bot.copy_media_group(message.chat.id, msg.chat.id, msg.id)
					except:
						if acc is None:
							print(f"**String Session is not Set - Skipped**")
						# try: handle_private(message,username,msgid)
						# except Exception as e: print(f"**Error** : __{e}__")
					time.sleep(3)
				links_force(username=uss, msgid=i).update_links()

# get the type of message
def get_message_type(msg: pyrogram.types.messages_and_media.message.Message):

	try:
		msg.photo.file_id
		return "Photo"
	except: pass

	try:
		msg.video.file_id
		return "Video"
	except: pass

# infinty polling
bot.run()