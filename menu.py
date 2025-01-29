from db_postgre import channel
from db_sqlite import channel as channel_sqlite

menu ='''\nHADES 0212\n
1. Cập nhật msg_end
2. Đồng bộ từ sqlite sang postgresql
3. Đồng bộ từ postgresql sang sqlite
'''
print(menu)
key_x = input("Vui lòng chọn giá trị: ")
match int(key_x):
    case 1:
        record = channel().get_all()
        for item in record:
            print(f"{item.id} - {item.username}")
        id = input("Chọn channel cần cập nhật: ")
        msg_end = input("Điền giá trị msg_end: ")
        try:
            channel(id = int(id), msgid_end = int(msg_end)).update_msg_end()
            print("SUCCESS")
        except:
            channel.reset()
    case 2:
        rc = channel_sqlite().get_all()
        try:
            channel().truncate_table()
            for r in rc:
                channel(links = r.links, username = r.username, msgid = r.msgid, msgid_end=r.msgid_end, target_channel = r.target_channel, media_type = r.media_type, note = r.note, status = r.status).save_db()
            print('Sync successful')
        except:
            print('Sync failed')
    case 3:
        rc = channel().get_all()
        try:
            channel_sqlite().truncate_table()
            for r in rc:
                channel_sqlite(id = r.id, links = r.links, username = r.username, msgid = r.msgid, msgid_end=r.msgid_end, target_channel = r.target_channel, media_type = r.media_type, note = r.note, status = r.status).save_db()
            print('Sync successful')
        except:
            print('Sync failed')

        