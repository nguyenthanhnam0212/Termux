import base64
import json
import os
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# package com.live.fox.utils.f;

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