import os
import asyncio
from pyrogram import Client, filters

from dotenv import load_dotenv
load_dotenv()

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
BOT_TOKEN = os.getenv('TOKEN')

Lib_dl = os.path.dirname(os.path.abspath(__file__))
WORKDIR = "/sdcard/Download"

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
            cwd=Lib_dl
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

        await client.send_video(
            chat_id=message.chat.id,
            video=latest_file,
            caption="✅ Xong!"
        )

        os.remove(latest_file)

    except Exception as e:
        await message.reply_text(f"❌ Lỗi: {e}")

app.run()
