import yt_dlp
from PIL import Image

class Youtube:
    def download(i, url_play):
        ydl_opts = {
            "format": "bv*+ba/b",
            "merge_output_format": "mp4",
            "ignoreerrors": True,
            "continue_dl": True,
            "outtmpl": f"{i+1}.%(ext)s",
            "writethumbnail": True,           # tải thumbnail
            "thumbnailformat": "jpg",
            "cachedir": False,              # không dùng cache
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Đang tải video {i+1} từ playlist...")
            info = ydl.extract_info(url_play, download=True)  # tải video