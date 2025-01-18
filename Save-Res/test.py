from pyrogram import Client
import os
from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv('TOKEN')
api_hash = os.getenv('API_HASH')
api_id = os.getenv('API_ID')

user_name = 'laosijighs'
target_id = -1002398906809
mess_id = 16205

with Client("save_content_x_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token) as bot:
	chat = bot.get_chat(user_name)
	try:
		bot.copy_message(chat_id=target_id, from_chat_id=chat.id, message_id=mess_id)
		print("SUCCESS")
	except Exception as e:
		print(f"ERROR: {e}")


	# msg = bot.get_messages('Timiys', 677)
	# print(str(msg.media).replace('MessageMediaType.','').strip())
