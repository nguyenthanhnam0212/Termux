import subprocess
import json
import os
import asyncio
from pyrogram import Client, filters
from db import _ABYSS
from pyrogram.types import InputMediaVideo, InputMediaPhoto

from dotenv import load_dotenv
load_dotenv()

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
BOT_TOKEN = os.getenv('TOKEN')

WORKDIR = os.path.dirname(os.path.abspath(__file__))


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

app = Client("save_content_x_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start_handler(client, message):
    await message.reply_text("Download Video Abyss")

@app.on_message(filters.command("upload"))
async def upload_handler(client, message):
    files = [f for f in os.listdir(WORKDIR) if f.endswith(".mp4")]
    if not files:
        await message.reply_text("❌ Không có file nào trong thư mục!")
        return
    for file in files:
        movie = os.path.join(WORKDIR, file)
        filename = os.path.basename(movie)
        filename_no_ext = os.path.splitext(filename)[0]
        movie_code = filename_no_ext.split("_")[0]

        width, height, duration = get_video_info(movie)

        try:

            detail = _ABYSS(movie_code = movie_code).get_inf()

            if detail.actor is not None or detail.actor != "":
                final_actor = ""
                actor = detail.actor.split(",")
                for i in actor:
                    final_actor = final_actor + f"#{i.replace(" ", "").strip()}   "

            caption = f"{detail.movie_name_vi} ({detail.movie_name_en})\n{final_actor}"

            image = detail.movie_image

            media = [
                InputMediaPhoto(
                    media=image
                ),
                InputMediaVideo(
                    media=movie,
                    width=width,
                    height=height,
                    duration=duration,
                    supports_streaming=True,
                    caption=caption
                )
            ]
            await message.reply_text("⬆️ Đang upload video ...")
            await app.send_media_group(
                chat_id=message.chat.id,
                media=media
            )
            _ABYSS(movie_code=movie_code, status=0).update_status()
        except:
            await message.reply_text("⬆️ Đang upload video ...")
            await app.send_video(chat_id=message.chat.id, video=movie, width=width, height=height, duration=duration, supports_streaming=True, caption=f"`{movie_code}`", parse_mode="Markdown")
        os.remove(movie)

@app.on_message(filters.text & ~filters.regex(r"^/"))
async def handle_download(client, message):
    try:
        ID = message.text.strip()
        await message.reply_text(f"▶️ Đang tải video `{ID}`...")

        print(WORKDIR)

        # chạy java trong async subprocess
        process = await asyncio.create_subprocess_exec(
            "java", "-jar", "abyss-dl.jar", ID, "h",
            cwd=WORKDIR
        )
        await process.wait()

        # tìm file mp4 trong WORKDIR
        downloaded_files = [f for f in os.listdir(WORKDIR) if f.endswith(".mp4")]
        if not downloaded_files:
            await message.reply_text("❌ Không tìm thấy file video sau khi tải!")
            return

        latest_file = max(
            [os.path.join(WORKDIR, f) for f in downloaded_files],
            key=os.path.getctime
        )

        width, height, duration = get_video_info(latest_file)

        await message.reply_text("⬆️ Đang upload video ...")

        try:

            detail = _ABYSS(movie_code = ID).get_inf()

            if detail.actor is not None or detail.actor != "":
                final_actor = ""
                actor = detail.actor.split(",")
                for i in actor:
                    final_actor = final_actor + f"#{i.replace(" ", "").strip()}   "


            caption = f"{detail.movie_name_vi} ({detail.movie_name_en})\n{final_actor}"

            image = detail.movie_image

            media = [
                InputMediaPhoto(
                    media=image
                ),
                InputMediaVideo(
                    media=latest_file,
                    width=width,
                    height=height,
                    duration=duration,
                    supports_streaming=True,
                    caption=caption
                )
            ]

            await app.send_media_group(
                chat_id=message.chat.id,
                media=media
            )
            _ABYSS(movie_code=ID, status=0).update_status()
        except:
            filename = os.path.basename(latest_file)
            filename_no_ext = os.path.splitext(filename)[0]
            movie_code = filename_no_ext.split("_")[0]
            await message.reply_text("⬆️ Đang upload video ...")
            await app.send_video(
                chat_id=message.chat.id,
                video = latest_file,
                width=width,
                height=height,
                duration=duration,
                supports_streaming=True,
                caption=f"`{movie_code}`"
            )
        os.remove(latest_file)

    except Exception as e:
        await message.reply_text(f"❌ Lỗi: {e}")

app.run()
