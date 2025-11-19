import subprocess
import json
import os
import asyncio
from pyrogram import Client, filters
# from db import _ABYSS
from poster import POSTER
from pyrogram.types import InputMediaVideo, InputMediaPhoto
import shutil
import datetime

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
    await message.reply_text("Download Video Abyss và chuyển vào Channel: -1001810577350")

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

        await message.reply_text("⬆️ Đang upload video ...")
        await app.send_video(chat_id=message.chat.id, video=movie, width=width, height=height, duration=duration, supports_streaming=True, caption=f"{movie_code}",)
        os.remove(movie)

@app.on_message(filters.command("delete"))
async def delete_handler(client, message):
    try:
        for file in os.listdir(WORKDIR):
            path = os.path.join(WORKDIR, file)
            if os.path.isfile(path) and file.endswith(".mp4"):
                os.remove(path)
            elif os.path.isdir(path):
                try:
                    shutil.rmtree(path)
                except Exception as e:
                    print(f"Không thể xóa folder {path}: {e}")
        await message.reply_text(f"🧹 Đã xóa")
    except Exception as e:
        await message.reply_text(f"❌ Lỗi khi xóa file: {e}")

@app.on_message(filters.text & ~filters.regex(r"^/"))
async def handle_download(client, message):
    text = message.text.strip()
    lines = text.splitlines()
    tap = range(56, 56 + len(lines))
    for t, i in zip(tap, lines):
        if "m3u8" in i:
            output = datetime.datetime.now().strftime("video_%Y%m%d_%H%M%S.mp4")
            url = i.strip()
            process = subprocess.Popen(
                [
                    "ffmpeg",
                    "-i", url, 
                    "-c:v", "copy",
                    "-c:a", "copy",
                    "-y", output
                ],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
            )
            print("Đang tải file ...")
            process.wait()
            print("Đã tải xong file !!!")
            downloaded_files = [f for f in os.listdir(WORKDIR) if f.endswith(".mp4")]
            if not downloaded_files:
                await status_msg.edit_text("❌ Không tìm thấy file sau khi download.")
                continue

            latest_file = max(
                [os.path.join(WORKDIR, f) for f in downloaded_files],
                key=os.path.getctime
            )

            width, height, duration = get_video_info(latest_file)

            image = "https://image.tmdb.org/t/p/w600_and_h900_bestv2/JnXbOUfeHUTlPJwZ1euqx9WLYs.jpg"
            media = [
                InputMediaPhoto(
                    media=image,
                    caption=f"Tom and Jerry Tales - {t}"
                ),
                InputMediaVideo(
                    media=latest_file,
                    width=width,
                    height=height,
                    duration=duration,
                    supports_streaming=True
                )
            ]
            print("Đang upload file !!!")
            await app.send_media_group(
                chat_id=message.chat.id,
                media=media
            )
            print("Hoàn thành upload !!!")
            os.remove(latest_file)
        else:
            try:
                if ":" in i:
                    mess = i.split(":")
                    ID = mess[0]
                    name_movie_en = mess[1]
                else:
                    ID = i.strip()
                    name_movie_en = ID
                status_msg  = await message.reply_text(f"▶️ Đang tải video `{ID}`...")

                cmd = f"java -jar abyss-dl.jar {ID} h"
                try:
                    subprocess.run(cmd, shell=True, cwd=WORKDIR)
                except:
                    await status_msg.edit_text("❌ Lỗi download bằng abyss-dl.jar")
                    continue
                
                # tìm file mp4 trong WORKDIR
                downloaded_files = [f for f in os.listdir(WORKDIR) if f.endswith(".mp4")]
                if not downloaded_files:
                    await status_msg.edit_text("❌ Không tìm thấy file sau khi download.")
                    continue

                latest_file = max(
                    [os.path.join(WORKDIR, f) for f in downloaded_files],
                    key=os.path.getctime
                )

                width, height, duration = get_video_info(latest_file)

                if (name_movie_en != "") and (name_movie_en != ID):
                    poster = POSTER.get_poster(name_movie_en)
                    if poster != "":
                        image = poster
                    else:
                        image = "https://image.tmdb.org/t/p/w600_and_h900_bestv2/y2vp0PhvCRY5jF3EiQWwXZ7Lsh8.jpg"
                    actor = POSTER.get_actor(name_movie_en)
                else:
                    image = "https://image.tmdb.org/t/p/w600_and_h900_bestv2/y2vp0PhvCRY5jF3EiQWwXZ7Lsh8.jpg"
                    actor = ""
                caption = f"({name_movie_en})\n{actor}"

                media = [
                    InputMediaPhoto(
                        media=image,
                        caption=caption
                    ),
                    InputMediaVideo(
                        media=latest_file,
                        width=width,
                        height=height,
                        duration=duration,
                        supports_streaming=True
                    )
                ]

                await status_msg.edit_text(f"Đang upload video: `{ID}`")
                await app.send_media_group(
                    chat_id=message.chat.id,
                    media=media
                )
                print("Hoàn thành upload !!!")

                os.remove(latest_file)
            except Exception as e:
                await message.reply_text(f"❌ Lỗi: {e}")
                print(f"❌ {i} - Lỗi: {e}")
                continue
app.run()
