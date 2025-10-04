import subprocess
import json
import os
import asyncio
import time
from pyrogram import Client, filters
from pyrogram.types import InputMediaVideo, InputMediaPhoto
from poster import POSTER
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


# === Progress callback ===
async def progress_callback(current, total, progress_msg, start_time):
    now = time.time()
    diff = now - start_time
    if diff == 0:
        diff = 1
    percent = current * 100 / total
    speed = current / diff
    eta = (total - current) / speed if speed > 0 else 0
    uploaded = current / (1024 * 1024)
    total_size = total / (1024 * 1024)
    text = f"⬆️ Upload: {percent:.1f}% ({uploaded:.1f}/{total_size:.1f} MB)\n⏱ ETA: {int(eta)}s"
    try:
        await progress_msg.edit_text(text)
    except:
        pass


app = Client("save_content_x_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


@app.on_message(filters.command("start"))
async def start_handler(client, message):
    list_ID = [{'ID': 'OrmhFwyxH', 'name_en': 'King Kong'}, {'ID': 's27ZchFjj', 'name_en': 'The Bourne Legacy'}, {'ID': 'h20jdcPg9', 'name_en': 'Safe'}, {'ID': 'OGePcsqcu', 'name_en': 'CJ7'}, {'ID': '6qGX3K5sUr', 'name_en': 'Naked Weapon'}, {'ID': 'OaWcGdeDHu', 'name_en': 'A Chinese Odyssey Part 2: Cinderella'}, {'ID': 'TcIdCDGbxG', 'name_en': 'Fist of Legend'}, {'ID': 'suzqSHzqA', 'name_en': 'Jason Bourne'}, {'ID': '3KczcF_T2', 'name_en': 'From Beijing with Love'}, {'ID': 'OVloH2149', 'name_en': 'Tricky Brains'}, {'ID': 'MN2mjN_JZ', 'name_en': 'God of Gamblers 3 BackTo Shanghai'}]

    for item in list_ID:
        ID = item['ID']
        name_movie_en = item['name_en']

        try:
            await message.reply_text(f"▶️ Đang tải video: {name_movie_en}")

            cmd = f"java -jar abyss-dl.jar {ID} h"
            try:
                subprocess.run(cmd, shell=True, cwd=WORKDIR)
                print("Tải xuống hoàn thành. Tiến hành upload...")
            except:
                print("❌ Lỗi không thể tải xuống ....")
                continue

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

            try:
                poster = POSTER.get_poster(name_movie_en)
                if poster != "":
                    image = poster
                else:
                    image = "https://image.tmdb.org/t/p/w600_and_h900_bestv2/y2vp0PhvCRY5jF3EiQWwXZ7Lsh8.jpg"
                actor = POSTER.get_actor(name_movie_en)
                caption = f"({name_movie_en})\n{actor}"

                # sau đó upload video có hiển thị % tiến trình
                progress_msg = await message.reply_text("⬆️ Bắt đầu upload video...")
                start_time = time.time()

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

                await app.send_media_group(
                    chat_id=message.chat.id,
                    media=media
                )

                await progress_msg.edit_text("✅ Upload hoàn thành!")
                print("Upload thành công")

            except Exception as e:
                print("❌ Upload kèm poster thất bại:", e)
                filename = os.path.basename(latest_file)
                filename_no_ext = os.path.splitext(filename)[0]
                movie_code = filename_no_ext.split("_")[0]

                progress_msg = await message.reply_text("⬆️ Đang upload video không kèm poster...")
                start_time = time.time()

                await app.send_video(
                    chat_id=message.chat.id,
                    video=latest_file,
                    width=width,
                    height=height,
                    duration=duration,
                    supports_streaming=True,
                    caption=f"`{movie_code}`",
                    progress=progress_callback,
                    progress_args=(progress_msg, start_time)
                )

                await progress_msg.edit_text("✅ Upload hoàn thành (không có poster)!")
                print("Upload thành công (no poster)")

            os.remove(latest_file)

        except Exception as e:
            await message.reply_text(f"❌ Lỗi: {e}")
            print(f"❌ Lỗi: {e}")
            continue


app.run()
