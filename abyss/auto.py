import subprocess
import json
import os
import asyncio
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

app = Client("save_content_x_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start_handler(client, message):
    list_ID = [{'ID': 'lk9EDMlen', 'name_en': 'Lara Croft Tomb Raider: The Cradle of Life'}, {'ID': 'pABMF1HM5', 'name_en': 'Lara Croft: Tomb Raider'}]
    for item in list_ID:
        ID = item['ID']
        name_movie_en = item['name_en']
        try:
            await message.reply_text(f"▶️ Đang tải video `{ID}`...")
            
            # chạy java trong async subprocess
            # process = await asyncio.create_subprocess_exec(
            #     "java", "-jar", "abyss-dl.jar", ID, "h",
            #     cwd=WORKDIR
            # )
            # await process.wait()

            cmd = f"java -jar abyss-dl.jar {ID} h"
            subprocess.run(cmd, shell=True, cwd=WORKDIR)

            print("Tải xuống hoàn thành. Tiến hành upload...")

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
                print("Upload thành công")
            except:
                filename = os.path.basename(latest_file)
                filename_no_ext = os.path.splitext(filename)[0]
                movie_code = filename_no_ext.split("_")[0]
                await message.reply_text("⬆️ Đang upload video không kèm poster...")
                await app.send_video(
                    chat_id=message.chat.id,
                    video = latest_file,
                    width=width,
                    height=height,
                    duration=duration,
                    supports_streaming=True,
                    caption=f"`{movie_code}`"
                )
                print("Upload thành công")
            os.remove(latest_file)

        except Exception as e:
            await message.reply_text(f"❌ Lỗi: {e}")
            print(f"❌ Lỗi: {e}")
app.run()
