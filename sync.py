from postgree import links_force as postgree_links_force
from sqlite_db import links_force as sqlite_links_force

def sqlite_to_postgree():
    rc = sqlite_links_force().get_all_record()
    try:
        postgree_links_force().truncate_save_links()
        for r in rc:
            postgree_links_force(links = r.links, username = r.username, msgid = r.msgid, target_channel = r.target_channel, media_type = r.media_type, note = r.note, status = r.status).save_to_links()
    except:
        result = 'Sync failed'
    result = 'Sync successful'
    return result

def postgree_to_sqlite():
    rc = postgree_links_force().get_all_record()
    try:
        sqlite_links_force().truncate_save_links()
        for r in rc:
            sqlite_links_force(links = r.links, username = r.username, msgid = r.msgid, target_channel = r.target_channel, media_type = r.media_type, note = r.note, status = r.status).save_to_links()
    except:
        result = 'Sync failed'
    result = 'Sync successful'
    return result 

X = input("Choose the database to sync: \n1. SQLite to Postgree\n2. Postgree to SQLite\n\n\n")
if X == "1":
    print (sqlite_to_postgree())
elif X == "2":
    print(postgree_to_sqlite())