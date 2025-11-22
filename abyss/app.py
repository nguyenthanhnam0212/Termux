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
import yt_dlp
from PIL import Image

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

@app.on_message(filters.command("hls"))
async def m3u8_handler(client, message):
    with open("hls.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()

        chaps = range(1, 1 + len(lines))

        for chap, line in zip(chaps, lines):
            url = line.strip()
            output = datetime.datetime.now().strftime("video_%Y%m%d_%H%M%S.mp4")
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
            print(f"Đang tải url: {url}")
            process.wait()
            print("Đã tải xong file !!!")
            downloaded_files = [f for f in os.listdir(WORKDIR) if f.endswith(".mp4")]
            if not downloaded_files:
                print("❌ Không tìm thấy file sau khi download.")
                continue

            latest_file = max(
                [os.path.join(WORKDIR, f) for f in downloaded_files],
                key=os.path.getctime
            )

            width, height, duration = get_video_info(latest_file)

            image = "https://image.tmdb.org/t/p/w600_and_h900_bestv2/Op0qUKIiVVblpFStjc3MpNaDbb.jpg"
            media = [
                InputMediaPhoto(
                    media=image,
                    caption=f"Tom and Jerry Collections (1940) - {chap}"
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

@app.on_message(filters.command("youtube"))
async def youtube_handler(client, message):
    playlist_url = "https://www.youtube.com/watch?v=p90V7QNJuX8&list=PLRzZKXQ7FcALbtvVlcKYHVtxpAg_VeGXm"
    for index in range(1, 3):
        ydl_opts = {
            "format": "bv*+ba/b",
            "merge_output_format": "mp4",
            "ignoreerrors": True,
            "continue_dl": True,
            "outtmpl": f"{index}.%(ext)s",
            "playlist_items": f"{index}",   # Chỉ duy nhất video theo index
            "writethumbnail": True,           # tải thumbnail
            "thumbnailformat": "jpg",
            "cachedir": False,              # không dùng cache
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Đang tải video {index} từ playlist...")
            ydl.download([playlist_url])

        files = [f for f in os.listdir(WORKDIR) if f.endswith(".mp4")]
        if not files:
            await message.reply_text("❌ Không có file nào trong thư mục!")
            return
        for file in files:
            movie = os.path.join(WORKDIR, file)
            os.remove(os.path.join(WORKDIR, f"{os.path.splitext(file)[0]}.jpg"))
            thumb_file_webp = os.path.join(WORKDIR, f"{os.path.splitext(file)[0]}.webp")
            im = Image.open(thumb_file_webp).convert("RGB")
            im.save(f"{index}.jpg", "JPEG")
            thumb_file = os.path.join(WORKDIR, f"{os.path.splitext(file)[0]}.jpg")

            width, height, duration = get_video_info(movie)

            print("Đang upload video ...")
            await app.send_video(chat_id=message.chat.id, video=movie, width=width, height=height, duration=duration, supports_streaming=True, thumb=thumb_file, caption=f"Thám Tử Lừng Danh Conan - Tập {index}")

            os.remove(thumb_file)
            os.remove(thumb_file_webp)
            os.remove(movie)

    print("Hoàn thành")

@app.on_message(filters.command("movie"))
async def movie_handler(client, message):
    with open("movie.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
        for i in lines:
            try:
                movie_inf = i.split("~")
                ID = movie_inf[0]
                name_movie_en = movie_inf[1]

                print(f"👉 Đang tải video `{ID}`...")

                cmd = f"java -jar abyss-dl.jar {ID} h"
                try:
                    subprocess.run(cmd, shell=True, cwd=WORKDIR)
                except:
                    print("❌ Lỗi download bằng abyss-dl.jar ❌")
                    continue
                
                # tìm file mp4 trong WORKDIR
                downloaded_files = [f for f in os.listdir(WORKDIR) if f.endswith(".mp4")]
                if not downloaded_files:
                    print("❌ Không tìm thấy file sau khi download.")
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

                print("👉 Đang upload video `{ID}`")
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
            

# Xóa toàn bộ file mp4 đã tải về trong folder WORKDIR
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
    for i in zip(lines):
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
                ),
                InputMediaVideo(
                    media=latest_file,
                    width=width,
                    height=height,
                    duration=duration,
                    supports_streaming=True
                )
            ]
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
