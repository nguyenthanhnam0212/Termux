import yt_dlp

playlist_url = "https://www.youtube.com/playlist?list=PLRzZKXQ7FcALbtvVlcKYHVtxpAg_VeGXm"

ydl_opts = {
    "quiet": True,
    "extract_flat": True  # chỉ lấy danh sách video, không load chi tiết từng video
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(playlist_url, download=False)

urls = []
titles = []

# Kiểm tra xem info có 'entries' (playlist) hay chỉ là 1 video
if 'entries' in info:
    for video in info['entries']:
        # url có thể ở key 'url' hoặc 'webpage_url'
        urls.append(video.get('url') or video.get('webpage_url'))
        titles.append(video.get('title'))
else:
    urls.append(info.get('url') or info.get('webpage_url'))
    titles.append(info.get('title'))

with open("data_youtube.txt", "a", encoding="utf-8") as f:
    for i, (title, url) in enumerate(zip(titles, urls), start=1):
        f.write(f"{url}\n")