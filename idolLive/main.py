from yylive import YYLive
from mmlive import MMLive
import json
import subprocess
import datetime
import time
import threading

class Idol():
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
            # else:
            #     array_nomal.append(i)
        array_dict = array_vip + array_nomal

        result = {"data": array_dict}
        json_str = json.dumps(result, ensure_ascii=False)
        return json_str
    

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

    print(f"👉 Đang ghi stream vào: {output}")
    return process

def timer(process):
    start_time = time.time()
    while process.poll() is None:  # ffmpeg vẫn đang chạy
        elapsed = int(time.time() - start_time)
        h = elapsed // 3600
        m = (elapsed % 3600) // 60
        s = elapsed % 60
        print(f"\r⏱️ Đã ghi được: {h:02d}:{m:02d}:{s:02d}", end="", flush=True)
        time.sleep(1)
    print("\n✅ Quay xong rồi!")
    
idols = Idol.get_inf_idol()
data = json.loads(idols)['data']
for i in data:
    print(f"{i['anchorId']} - {i['anchorNickname']}")

id = input("Nhập ID: ")

match len(id.strip()):
    case 10:
        link = MMLive.get_link(id.strip())
    case 19:
        src = YYLive.get_src(id.strip())
        link = YYLive.convert_src(src)


process = record(link, id.strip())
timer_thread = threading.Thread(target=timer, args=(process,), daemon=True)
timer_thread.start()
process.wait()