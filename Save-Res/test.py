from pyrogram import Client
import os
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

bot_token = os.getenv('TOKEN')
api_hash = os.getenv('API_HASH')
api_id = os.getenv('API_ID')

user_name = 'Timiys'
target_id = -1002333974972
mess_id = 577

with Client("save_content_x_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token) as bot:
	chat = bot.get_chat('Timiys')
	try:
		bot.copy_message(chat_id=target_id, from_chat_id=chat.id, message_id=mess_id)
		print("SUCCESS")
	except Exception as e:
		print(f"ERROR: {e}")
