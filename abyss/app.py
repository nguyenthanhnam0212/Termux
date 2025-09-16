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

app = Client("abyss_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start_handler(client, message):
    await message.reply_text("Download Video Abyss")

@app.on_message(filters.text & ~filters.command("start"))
async def handle_download(client, message):
    try:
        ID = message.text.strip()
        await message.reply_text(f"▶️ Đang tải video `{ID}`...")

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

        await message.reply_text("⬆️ Đang upload video lên Telegram...")

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
                caption=caption,
                supports_streaming=True
            )
        ]

        await client.send_media_group(
            chat_id=message.chat.id,
            media=media
        )

        # await client.send_video(
        #     chat_id=message.chat.id,
        #     video=latest_file,
        #     caption=caption,
        #     supports_streaming=True
        # )

        _ABYSS(movie_code=ID, status=0).update_status()
        os.remove(latest_file)

    except Exception as e:
        await message.reply_text(f"❌ Lỗi: {e}")

app.run()
