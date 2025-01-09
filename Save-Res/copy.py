import pyrogram
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant, InviteHashExpired, UsernameNotOccupied
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import time
import os
import threading
import json

from sqlite_db import temp_db, links_force
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

# download status
def downstatus(statusfile,message):
	while True:
		if os.path.exists(statusfile):
			break

	time.sleep(3)      
	while os.path.exists(statusfile):
		with open(statusfile,"r") as downread:
			txt = downread.read()
		try:
			bot.edit_message_text(message.chat.id, message.id, f"__Downloaded__ : **{txt}**")
			time.sleep(10)
		except:
			time.sleep(5)


# upload status
def upstatus(statusfile,message):
	while True:
		if os.path.exists(statusfile):
			break

	time.sleep(3)      
	while os.path.exists(statusfile):
		with open(statusfile,"r") as upread:
			txt = upread.read()
		try:
			bot.edit_message_text(message.chat.id, message.id, f"__Uploaded__ : **{txt}**")
			time.sleep(10)
		except:
			time.sleep(5)


# progress writter
def progress(current, total, message, type):
	with open(f'{message.id}{type}status.txt',"w") as fileup:
		fileup.write(f"{current * 100 / total:.1f}%")


# start command
@bot.on_message(filters.command(["start"]))
def send_start(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
	bot.send_message(message.chat.id, f"__👋 Hi **{message.from_user.mention}**, I am Save Restricted Bot")


@bot.on_message(filters.text)
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
	for i in tqdm(range(from_id, to_id), desc="Forwarding", unit="Post"):
		message.text = f"https://t.me/{uss}/{i}"
		print(f"\rCompleted ID: {i} / {to_id-1}  ", end='', flush=True)
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

				# private
				if "https://t.me/c/" in message.text:
					chatid = int("-100" + datas[4])
					
					if acc is None:
						bot.send_message(message.chat.id,f"**String Session is not Set**")
						return
					
					handle_private(message,chatid,msgid)
					# try: handle_private(message,chatid,msgid)
					# except Exception as e: bot.send_message(message.chat.id,f"**Error** : __{e}__")
				
				# bot
				elif "https://t.me/b/" in message.text:
					username = datas[4]
					
					if acc is None:
						bot.send_message(message.chat.id,f"**String Session is not Set**")
						return
					try: handle_private(message,username,msgid)
					except Exception as e: bot.send_message(message.chat.id,f"**Error** : __{e}__")

				# public
				else:
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
				# wait time
				# time.sleep(3)

# handle private
def handle_private(message: pyrogram.types.messages_and_media.message.Message, chatid: int, msgid: int):
		msg: pyrogram.types.messages_and_media.message.Message = acc.get_messages(chatid,msgid)
		msg_type = get_message_type(msg)

		if "Text" == msg_type:
			bot.send_message(message.chat.id, msg.text, entities=msg.entities)
			return

		smsg = bot.send_message(message.chat.id, '__Downloading__')
		dosta = threading.Thread(target=lambda:downstatus(f'{message.id}downstatus.txt',smsg),daemon=True)
		dosta.start()
		file = acc.download_media(msg, progress=progress, progress_args=[message,"down"])
		os.remove(f'{message.id}downstatus.txt')

		upsta = threading.Thread(target=lambda:upstatus(f'{message.id}upstatus.txt',smsg),daemon=True)
		upsta.start()
		
		if "Video" == msg_type:
			try: 
				thumb = acc.download_media(msg.video.thumbs[0].file_id)
			except: thumb = None
			bot.send_video(message.chat.id, file, duration=msg.video.duration, width=msg.video.width, height=msg.video.height, thumb=thumb, caption=msg.caption, caption_entities=msg.caption_entities, progress=progress, progress_args=[message,"up"])
			if thumb != None: os.remove(thumb)

		elif "Photo" == msg_type:
			bot.send_photo(message.chat.id, file, caption=msg.caption, caption_entities=msg.caption_entities)

		os.remove(file)
		if os.path.exists(f'{message.id}upstatus.txt'): os.remove(f'{message.id}upstatus.txt')
		bot.delete_messages(message.chat.id,[smsg.id])


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
