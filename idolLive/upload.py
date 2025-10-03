import subprocess
import json
import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InputMediaVideo, InputMediaPhoto
from tqdm import tqdm

from dotenv import load_dotenv
load_dotenv()

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
BOT_TOKEN = os.getenv('TOKEN')

WORKDIR = f"/sdcard/Download/"


def get_video_info(path: str):
    cmd = [
        "ffprobe", "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height,duration",
        "-of", "json", path
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    info = json.loads(result.stdout)
    stream = info["streams"][0]
    width = int(stream["width"])
    height = int(stream["height"])
    duration = int(float(stream.get("duration", 0)))
    return width, height, duration

def generate_thumb(video_path: str, thumb_path: str):
    """
    Lấy 1 frame làm thumbnail (ví dụ ở giây thứ 5).
    """
    cmd = [
        "ffmpeg", "-y", "-i", video_path,
        "-ss", "5", "-vframes", "1",
        "-vf", "scale=320:-1",  # scale nhỏ lại cho nhẹ
        thumb_path
    ]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

app = Client("abyss_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start_handler(client, message):
    await message.reply_text("Upload Video from Downloaded files")

@app.on_message(filters.command("upload"))
async def upload_handler(client, message):
    files = [f for f in os.listdir(WORKDIR) if f.endswith(".mp4")]
    if not files:
        await message.reply_text("❌ Không có file nào trong thư mục!")
        return
    for file in files:
        movie = os.path.join(WORKDIR, file)
        thumb_file = os.path.join(WORKDIR, f"{os.path.splitext(file)[0]}.jpg")
        generate_thumb(movie, thumb_file)

        width, height, duration = get_video_info(movie)

        await message.reply_text("⬆️ Đang upload video ...")
        await app.send_video(chat_id=message.chat.id, video=movie, width=width, height=height, duration=duration, supports_streaming=True, thumb=thumb_file)

        os.remove(thumb_file)
        os.remove(movie)

app.run()
