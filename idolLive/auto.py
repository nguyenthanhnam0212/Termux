from yylive import YYLive
from mmlive import MMLive
import json
import subprocess
import datetime
import time
import threading
import os

# Danh sách idol cần auto record
IDOL_LIST = [
    2025661563, 2026955894, 2023560570,
    "1888143101879033858", "1967187279232364545", "1970139445251002370",
    "1917130658326405122"
]

class Idol:
    @staticmethod
    def get_inf_idol():
        array_dict = []
        array_nomal = []
        array_vip = []
        try:
            mmlive = MMLive.get_RoomInfo()
        except:
            mmlive = []
        try:
            yylive = YYLive.get_RoomInfo()
        except:
            yylive = []

        data = mmlive + yylive
        
        for i in data:
            if i['type'] in [2, 1]:
                array_vip.append(i)
            else:
                array_nomal.append(i)
        array_dict = array_vip + array_nomal

        result = {"data": array_dict}
        return result


def record(link, anchor_id):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output = f"/sdcard/Download/{anchor_id}_{timestamp}.mp4"

    process = subprocess.Popen(
        [
            "ffmpeg",
            "-i", link,
            "-c:v", "copy",
            "-c:a", "copy",
            "-y", output
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT
    )
    return process


def timer(process, anchorNickname):
    start_time = time.time()
    while process.poll() is None:  # ffmpeg vẫn đang chạy
        elapsed = int(time.time() - start_time)
        h = elapsed // 3600
        m = (elapsed % 3600) // 60
        s = elapsed % 60
        print(f"\r⏱️ {anchorNickname} - Đã ghi được: {h:02d}:{m:02d}:{s:02d}", end="", flush=True)
        time.sleep(1)
    print(f"\n✅ {anchorNickname} quay xong rồi!")


def record_idol(i):
    anchorId = str(i['anchorId'])
    live_type = i['type']
    liveId = i['liveId']
    anchorNickname = i['anchorNickname']

    try:
        if len(anchorId) == 10:
            link = MMLive.get_link(anchorId=anchorId, liveId=liveId, live_type=live_type)
        elif len(anchorId) == 19:
            src = YYLive.get_src(anchorId)
            link = YYLive.convert_src(src)
        else:
            print(f"❌ Không nhận diện được link của {anchorNickname}")
            return
    except Exception as e:
        print(f"❌ Lỗi lấy link {anchorNickname}: {e}")
        return

    print(f"▶️ Bắt đầu record {anchorNickname}")
    process = record(link, anchorId)

    # chạy timer trong thread riêng
    timer_thread = threading.Thread(target=timer, args=(process, anchorNickname), daemon=True)
    timer_thread.start()

    process.wait()


def main_loop():
    # Lưu lại các idol đang record (tránh record trùng nhiều lần)
    active_recordings = {}

    while True:
        try:
            idols = Idol.get_inf_idol()['data']
        except Exception as e:
            print(f"❌ Lỗi lấy danh sách idol: {e}")
            idols = []

        for i in idols:
            anchorId = str(i['anchorId'])
            if anchorId in map(str, IDOL_LIST):
                if anchorId not in active_recordings or active_recordings[anchorId].poll() is not None:
                    # Chưa record hoặc record trước đã kết thúc
                    t = threading.Thread(target=record_idol, args=(i,), daemon=True)
                    t.start()
                    active_recordings[anchorId] = None  # đánh dấu là đang chạy

        print("⏳ Chờ 10 phút rồi quét lại...")
        time.sleep(600)


if __name__ == "__main__":
    main_loop()
