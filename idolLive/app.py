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
            if not isinstance(mmlive, list):
                print(mmlive)
                mmlive = []
        except:
            mmlive = []
        try:
            yylive = YYLive.get_RoomInfo()
            if not isinstance(yylive, list):
                print(yylive)
                yylive = []
        except:
            yylive = []
        try:
            qqlive = QQLive.get_RoomInfo()
            if not isinstance(qqlive, list):
                print(qqlive)
                qqlive = []
        except:
            qqlive = []
        try:
            hot51 = Hot51.get_RoomInfo()
            if not isinstance(hot51, list):
                print(hot51)
                hot51 = []
        except:
            hot51 = []

        data = mmlive + yylive + qqlive + hot51
        
        for i in data:
            if i['type'] in [1, 2]:
                array_vip.append(i)
            else:
                array_nomal.append(i)
        array_dict = array_vip + array_nomal

        result = {"data": array_dict}
        json_str = json.dumps(result, ensure_ascii=False)
        return json_str

    def link_record(anchor_id, liveId, live_type, source):        
        match source:
            case 'MMLive':
                link = MMLive.get_link(anchorId = anchor_id, liveId= liveId, live_type = live_type)
            case 'YYLive':
                src = YYLive.get_src(anchor_id)
                if src == 'Offline':
                    return None
                link = YYLive.convert_src(src)
            case 'Hot51':
                src = Hot51.get_src(anchor_id)
                if src == 'Offline':
                    return None
                link = Hot51.convert_src(src)
            case 'QQLive':
                link_decode, key, iv = QQLive.get_link(anchorId = anchor_id, liveId= liveId, live_type = live_type)
                link = QQLive.convert_src(link_decode, key, iv)
        return link


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


def timer(anchor_id, liveId, live_type, source):
    link = Idol.link_record(anchor_id, liveId, live_type, source)
    if link is None:
        print("❌ Idol offline ngay từ đầu.")
        return
    
    print("🎬 Bắt đầu ghi ...")
    process = record(link, anchor_id)
    start_time = time.time()

    while True:
        # FFmpeg đang chạy
        while process.poll() is None:
            elapsed = int(time.time() - start_time)
            h = elapsed // 3600
            m = (elapsed % 3600) // 60
            s = elapsed % 60
            print(f"\r⏱️ Đã ghi được: {h:02d}:{m:02d}:{s:02d}", end="", flush=True)
            time.sleep(1)
        if source in ["YYLive", "Hot51"]:
            link_new = Idol.link_record(anchor_id, liveId, live_type, source)
        elif source == "MMLive":
            mmlive = MMLive.get_RoomInfo()
            for i in mmlive:
                if i in anchor_id:
                    link_new = Idol.link_record(i['anchorId'], i['liveId'], i['type'], source)
                    break
        elif source == "QQLive":
            qqlive = QQLive.get_RoomInfo()
            for i in qqlive:
                if i in anchor_id:
                    link_new = Idol.link_record(i['anchorId'], i['liveId'], i['type'], source)
                    break


        if link_new is None:
            print("❌ Idol offline — stop record.")
            break

        print("🎬 Bắt đầu ghi file mới ...")
        process = record(link_new, anchor_id)
        start_time = time.time()


# ===== MAIN PROGRAM ======

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

print(f"🎥 Đang record: {anchorNickname}\n")

timer_thread = threading.Thread(target=timer, args=(id.strip(), liveId, live_type, app), daemon=True)
timer_thread.start()
timer_thread.join()