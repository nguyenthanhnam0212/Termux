from yylive import YYLive
from mmlive import MMLive
import json
import subprocess
import datetime

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

print(link)

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
output = f"/sdcard/Download/{id.strip()}_{timestamp}.mp4"

process = subprocess.Popen(
    [
        "ffmpeg",   # Trên Termux đã cài bằng pkg install ffmpeg
        "-i", link,
        "-c:v", "copy",
        "-c:a", "copy",
        "-y", output
    ],
    stdin=subprocess.PIPE,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.STDOUT   # hoặc subprocess.DEVNULL nếu không muốn log
)