from yylive import YYLive
from mmlive import MMLive
from hot51 import Hot51
from qqlive import QQLive
import json
import subprocess
import datetime
import time
import threading
import os

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
        try:
            qqlive = QQLive.get_RoomInfo()
        except:
            qqlive = []
        try:
            hot51 = Hot51.get_RoomInfo()
        except:
            hot51 = []

        data = mmlive + yylive + qqlive + hot51
        
        for i in data:
            if i['type'] in [2, 1]:
                array_vip.append(i)
            else:
                array_nomal.append(i)
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
    if i['anchorId'] not in [2021923813, 2022009695, 2023017337, 2022626776, 2027533958, 2027620165, 2027620341, 2027620016,
                             "1598549684535160834", 
                             "1900493761044578305", 
                             "1876551124468125698", 
                             "1596380393802973185", 
                             "1825818035638411266", 
                             "1665335675225264129", 
                             "1872165888673222657", 
                             "1596373615518302210", 
                             "1598549452099416065", 
                             "1801235281629249538", 
                             "1792202132639969281",
                             "1954886569027305473",
                             "1907097473055928322",
                             "1787831695819378689"]:
        print(f"{i['anchorId']} - {i['anchorNickname']}")

id = input("Nhập ID: ")

os.system('cls' if os.name == 'nt' else 'clear')

for i in data:
    if str(i['anchorId']) == id.strip():
        live_type = i['type']
        liveId = i['liveId']
        anchorNickname = i['anchorNickname']
        app = i['source']
        break

match app:
    case 'MMLive':
        link = MMLive.get_link(anchorId = id.strip(), liveId= liveId, live_type = live_type)
    case 'YYLive':
        src = YYLive.get_src(id.strip())
        link = YYLive.convert_src(src)
    case 'Hot51':
        src = Hot51.get_src(id.strip())
        link = Hot51.convert_src(src)
    case 'QQLive':
        link_decode, key, iv = QQLive.get_link(anchorId = id.strip(), liveId= liveId, live_type = live_type)
        link = QQLive.convert_src(link_decode, key, iv)

print(f"Đang record {anchorNickname}")

process = record(link, id.strip())
timer_thread = threading.Thread(target=timer, args=(process,), daemon=True)
timer_thread.start()
process.wait()