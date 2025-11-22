import yt_dlp
from PIL import Image
import os

class Youtube:
    def download(file_name, url_play):
        WORKDIR = os.path.dirname(os.path.abspath(__file__))
        ydl_opts = {
            "format": "bv*+ba/b",
            "merge_output_format": "mp4",
            "ignoreerrors": True,
            "continue_dl": True,
            "outtmpl": f"{file_name}.%(ext)s",
            "writethumbnail": True,           # tải thumbnail
            "thumbnailformat": "jpg",
            "cachedir": False,              # không dùng cache
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url_play, download=True)  # tải video
            title = info['title']
        thumb_file_webp = os.path.join(WORKDIR, f"{file_name}.webp")
        im = Image.open(thumb_file_webp).convert("RGB")
        im.save(f"{file_name}.jpg", "JPEG")
        os.remove(thumb_file_webp)
        return title