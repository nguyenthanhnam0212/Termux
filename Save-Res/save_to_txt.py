import json

class note:
    def get_inf(id):
        with open("Save-Res/json.txt", "r") as file:
            data = json.load(file)
        for record in data['data']:
            if record['id'] == id:
                user_name = record['user_name']
                msg_from = record['msg_from']
                msg_to = record['msg_to']
                target_id = record['target_id']
                media = record['media']
                break
        return user_name, msg_from, msg_to, target_id, media
    
    def update_json(user_name, msg_from):
        with open("Save-Res/json.txt", "r", encoding="utf-8") as file:
            data = json.load(file)
        for record in data['data']:
            if record['user_name'] == user_name:
                record['msg_from'] = msg_from
        with open("Save-Res/json.txt", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def get_all_user():
        result = ""
        with open("Save-Res/json.txt", "r", encoding="utf-8") as file:
            data = json.load(file)
            for i in data['data']:
                result = result + f"{i['id']} - {i['user_name']} - {i['media']}\n" 
        return result.strip()


