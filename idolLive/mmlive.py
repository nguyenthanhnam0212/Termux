import requests
from datetime import datetime, timezone, timedelta
import json
import base64
import os
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

class en_de_aes:

    def encode_request(req : dict) -> dict:
        
        MASTER_KEY = b"ajqfy63c7hrpb67f"
        IV = b"vpq8agq6zvwmddqj"

        def aes_encrypt(data: bytes, key: bytes, iv: bytes) -> bytes:
            cipher = AES.new(key, AES.MODE_CBC, iv)
            return cipher.encrypt(pad(data, AES.block_size))
        
        """
        Tạo body request {abc, qwe} từ JSON gốc
        """
        payload = json.dumps(req, ensure_ascii=False).encode("utf-8")

        # 1. sinh random 16 chữ số (SessionKey)
        session_key = "".join([str(os.urandom(1)[0] % 10) for _ in range(16)]).encode("utf-8")

        # 2. mã hoá session_key bằng master key
        enc_session = aes_encrypt(session_key, MASTER_KEY, IV)
        abc = str(int(time.time() * 1000)) + base64.b64encode(enc_session).decode("utf-8")

        # 3. mã hoá payload bằng session_key
        enc_payload = aes_encrypt(payload, session_key, IV)
        qwe = base64.b64encode(enc_payload).decode("utf-8")
        body = {"abc": abc, "qwe": qwe}

        return body


    def decode_response(res: dict) -> dict:
        MASTER_KEY = b"ajqfy63c7hrpb67f"
        IV = b"vpq8agq6zvwmddqj"

        def aes_decrypt(data: bytes, key: bytes, iv: bytes) -> bytes:
            cipher = AES.new(key, AES.MODE_CBC, iv)
            return unpad(cipher.decrypt(data), AES.block_size)

        """
        Giải mã body response {abc, qwe} thành JSON gốc
        """
        abc = res["abc"]
        qwe = res["qwe"]

        # 1. Bỏ 13 ký tự đầu của abc
        enc_session_b64 = abc[13:]
        enc_session = base64.b64decode(enc_session_b64)

        # 2. Giải mã ra session_key
        session_key = aes_decrypt(enc_session, MASTER_KEY, IV)

        # 3. Giải mã payload bằng session_key
        enc_payload = base64.b64decode(qwe)
        plain_json = aes_decrypt(enc_payload, session_key, IV).decode("utf-8")

        # with open(f"decode.json", "w", encoding="utf-8") as f:
        #     f.write(plain_json)

        return json.loads(plain_json)
    
class MMLive:
    token = None   # biến class để giữ token

    @classmethod
    def login(cls):
        url = "https://gateway.mm-obtain.com/center-client/sys/auth/new/phone/login"
        header = {
            "Accept-Encoding": "gzip",
            "Accept-Language": "vi",
            "appId": "MMLive",
            "Connection":"Keep-Alive",
            "Content-Length":"642",
            "Content-Type":"application/json; charset=utf-8",
            "Host":"gateway.mm-obtain.com",
            "N-L":"Y",
            "NEW-PK":"1",
            "os":"1",
            "P-AE":"1",
            "P-G":"N",
        }
        make_body = {
            "mobile": "0923101027",
            "password": "Hades0212",
            "os": "1",
            "version": "15.0",
            "udid": "",
            "model": "S25_Ultra"
        }

        body = en_de_aes.encode_request(make_body)
        res = requests.post(url, json=body, headers=header)
        if res.status_code != 200:
            return f"Error - HTTP {res.status_code}"
        else:
            data = res.json()
            decode_data = en_de_aes.decode_response(data)
            cls.token = decode_data['data']['token'] 
            return cls.token
        
    @classmethod
    def get_token(cls):
        if cls.token is None:   # nếu chưa có token thì login 1 lần
            cls.login()
        return cls.token
    
    @classmethod
    def get_RoomInfo(cls):
        token = cls.get_token()
        url = "https://gateway.mm-obtain.com/live-client/live/new/4231/1529/list"
        headers = {
            "Accept-Encoding": "gzip",
            "Accept-Language": "vi",
            "appId": "MMLive",
            "Authorization": f"HSBox {token}",
            "Connection":"Keep-Alive",
            "Content-Length":"834",
            "Content-Type":"application/json; charset=utf-8",
            "Host":"gateway.mm-obtain.com",
            "N-L":"Y",
            "NEW-PK":"1",
            "os":"1",
            "P-AE":"1",
            "P-G":"N",
        }

        make_body = {
            "token": token,
            "type": 1
        }
        body = en_de_aes.encode_request(make_body)
        response = requests.post(url, headers=headers, json=body)
        if response.status_code != 200:
            return f"Error - HTTP {response.status_code}"
        else:
            array_dict = []
            array_toy = []
            array_nomal = []
            array_vip = []

            data_encode = response.json()
            data_decode = en_de_aes.decode_response(data_encode)
            # with open(f"full.json", "w", encoding="utf-8") as f:
            #     f.write(json.dumps(data_decode, ensure_ascii=False, indent=4))
            data = data_decode['data']
            for i in data:
                if i['type'] == 2 or i['type'] == 1:
                    array_vip.append({"anchorId": i['anchorId'], "anchorNickname": f"{i['nickname'].ljust(20)}💰", "headPortrait": i['avatar'], "liveId": i['liveId'], "type": i['type'], "source": "MMLive"})
                else:
                    if i['toy'] == 1:
                        array_toy.append({"anchorId": i['anchorId'], "anchorNickname": f"{i['nickname'].ljust(20)}🍆", "headPortrait": i['avatar'], "liveId": i['liveId'], "type": i['type'], "source": "MMLive"})
                    else:
                        array_nomal.append({"anchorId": i['anchorId'], "anchorNickname": i['nickname'], "headPortrait": i['avatar'], "liveId": i['liveId'], "type": i['type'], "source": "MMLive"})
            array_dict = array_vip + array_toy + array_nomal
            return array_dict

    @classmethod        
    def get_link(cls, anchorId, liveId, live_type):
        token = cls.get_token()
        url = "https://gateway.mm-obtain.com/live-client/live/inter/room/220"
        header = {
            "Accept-Encoding": "gzip",
            "Accept-Language": "vi",
            "appId": "MMLive",
            "Authorization": f"HSBox {token}",
            "Connection":"Keep-Alive",
            "Content-Length":"898",
            "Content-Type":"application/json; charset=utf-8",
            "Host":"gateway.mm-obtain.com",
            "N-L":"Y",
            "NEW-PK":"1",
            "os":"1",
            "P-AE":"1",
            "P-G":"N",
            "versionTag": "Y",
            "X-AppVersion": "2.6.1",
            "X-Language": "YN",
            "X-Sign": "3939BF7D7161CA6FC184CEF297B4E9D8",
            "X-Timestamp": "1757257189538",
            "X-U": "2023691776",
            "X-UDID": "1af7173fecc68150"
        }
        make_body = {
            "token": token,
            "liveId": liveId,
            "anchorId": anchorId,
            "type": live_type,
        }
        body = en_de_aes.encode_request(make_body)
        res = requests.post(url, json=body, headers=header)
        if res.status_code != 200:
            return None
        else:
            data =  res.json()
            decode_data = en_de_aes.decode_response(data)
            return decode_data['data']['pullStreamUrl']