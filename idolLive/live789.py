import requests
import base64
from Crypto.Cipher import AES
from wcwidth import wcswidth

class _789Live:

    def get_RoomInfo():
        url = "https://cdn.gocdns.com/560/api/plr/zbliv/v5/public/live/lives?pageNum=1&pageSize=200&labelId=1&area"
        headers = {
            "Accept-Encoding": "gzip",
            "area": "VN",
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic YXBwLXBsYXllcjphcHBQbGF5ZXIyMDIxKjk2My4=",
            "client-type": "1",
            "Connection": "Keep-Alive",
            "Content-Length": "0",
            "Host": "cdn.gocdns.com",
            "dev-type": "android_samsung_S25_Ultra",
            "device": "a4d92c8f1e37b6a59f08c7d4b2e913cd",
            "system-version": "15.0",
            "User-Agent": "okhttp/4.10.0",
            "locale-language": "VIT",
            "merchantId": "560",
            "time-zone": "GMT+07:00",
            "versionCode": "572"
        }
        response = requests.post(url, headers=headers)
        if response.status_code != 200:
            return f"Error - HTTP {response.status_code}"
        else:
            data = response.json()['data']['records']
            array_dict = []
            array_nomal = []
            array_vip = []
            for i in data:
                if i['payType'] == 2:
                    array_vip.append({"anchorId": i['anchorId'], "anchorNickname": f"{i['anchorNickname']}\n💰", "headPortrait": i['coverUrl'], "liveId": "", "type": i['payType'], "source": "789Live"})
                else:
                    array_nomal.append({"anchorId": i['anchorId'], "anchorNickname": i['anchorNickname'], "headPortrait": i['coverUrl'], "liveId": "", "type": i['payType'], "source": "789Live"})
            array_dict = array_vip + array_nomal
            return array_dict

    def get_src(anchorId):
        url = "https://cdn.gocdns.com/560/api/plr/zbliv/v3/public/live/room-info"

        body = {
            "anchorId": anchorId,
            "spH5": 1
            }

        headers = {
            "Accept-Encoding": "gzip",
            "area": "VN",
            "Authorization": f"Basic YXBwLXBsYXllcjphcHBQbGF5ZXIyMDIxKjk2My4=",
            "client-type": "1",
            "Connection": "Keep-Alive",
            "Content-Length": "43",
            "Content-Type": "application/json;charset=UTF-8",
            "dev-type": "android_samsung_S25_Ultra",
            "device": "a4d92c8f1e37b6a59f08c7d4b2e913cd",
            "Host": "cdn.gocdns.com",
            "locale-language": "VIT",
            "merchantId": "560",
            "system-version": "15.0",
            "time-zone": "GMT+07:00",
            "User-Agent": "okhttp/4.10.0",
            "versionCode": "572"
        }

        response = requests.post(url, json=body, headers=headers)
        data = response.json()
        try:
            # link_play = data['data']['pullAddr']
            try:
                link_play = data['data']['unlDefPa']
            except:
                link_play = data['data']['unlLowPa']
            return link_play
        except:
            return {'Offline'}

    def convert_src(link):

        KEY = b"star@livega*963."
        IV  = b"0608040307010502"

        raw = base64.b64decode(link)
        cipher = AES.new(KEY, AES.MODE_CBC, IV)
        decrypted = cipher.decrypt(raw)
        pad_len = decrypted[-1]
        if pad_len < 1 or pad_len > 16:
            return "Error - Padding không hợp lệ"
        else:
            unpadded = decrypted[:-pad_len]
        return unpadded.decode("utf-8")