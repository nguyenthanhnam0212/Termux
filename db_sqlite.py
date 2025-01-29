from sqlalchemy import create_engine, Column, Integer, String, MetaData, BigInteger, func, text, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Khởi tạo cơ sở dữ liệu SQLite
DATABASE_URL = "sqlite:///Hades.db"  # Đường dẫn tới file SQLite
engine = create_engine(DATABASE_URL, echo=False)  # echo=True để log các câu lệnh SQL
Base = declarative_base()

class temp_storage(Base):
    __tablename__ = "temp_storage"
    id = Column(Integer, primary_key=True)
    file_id_photo = Column(String)
    file_id_video = Column(String)
    caption = Column(String)
    actor = Column(String)
    video_duration = Column(Integer)
    file_size = Column(BigInteger)
    note = Column(String)
    status = Column(Integer)

class channel_info(Base):
    __tablename__ = "channel_info"
    id = Column(Integer, primary_key=True)
    links = Column(String)
    username = Column(String)
    msgid = Column(Integer)
    msgid_end = Column(Integer)
    target_channel = Column(Integer)
    media_type = Column(String)
    note = Column(String)
    status = Column(Integer)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

class temp_db():
    def __init__(self, file_id_photo = None, file_id_video = None, caption= None, actor = None, video_duration = None, file_size = None, note = None, status = 1):
        self.file_id_photo = file_id_photo
        self.file_id_video = file_id_video
        self.caption = caption
        self.actor = actor
        self.video_duration = video_duration
        self.file_size = file_size
        self.note = note
        self.status = status

    def save_to_temp(self):
        sql = temp_storage(file_id_photo=self.file_id_photo, file_id_video = self.file_id_video, caption = self.caption, actor = self.actor, video_duration = self.video_duration, file_size = self.file_size, note = self.note, status = self.status)
        session.add(sql)
        session.commit()
        session.close()

    def get_from_temp(self):
        record = session.query(temp_storage).filter(temp_storage.status == 1).order_by(desc(temp_storage.video_duration), desc(temp_storage.file_size)).all()
        return record
    
    def truncate_temp(self):
        session.execute(text("DELETE FROM temp_storage"))
        session.commit()
        session.close()

    def update_temp(self):
        session.query(temp_storage).update({temp_storage.status: 0})
        session.commit()
        session.close()

    def num_record():
        var = session.query(func.count()).select_from(temp_storage).filter(temp_storage.status == 1).scalar()
        session.close()
        return var

    def reset():
        session.rollback()

class channel():
    def __init__(self, id = None, links = None, username = None, msgid = None, msgid_end = None, target_channel = None, media_type = None, note = None, status = 1):
        self.id = id
        self.links = links
        self.username = username
        self.msgid = msgid
        self.msgid_end = msgid_end
        self.target_channel = target_channel
        self.media_type = media_type
        self.note = note
        self.status = status

    def save_db(self):
        sql = channel_info(links = self.links, username = self.username, msgid = self.msgid, msgid_end = self.msgid_end, target_channel = self.target_channel, media_type = self.media_type, note = self.note, status = self.status)
        session.add(sql)
        session.commit()
        session.close()

    def update_links(self):
        session.query(channel_info).filter(channel_info.username == self.username).update({channel_info.msgid: self.msgid})
        session.commit()
        session.close()

    def update_msg_end(self):
        session.query(channel_info).filter(channel_info.id == self.id).update({channel_info.msgid_end: self.msgid_end})
        session.commit()
        session.close()

    def get_inf(id):
        record = session.query(channel_info).filter(channel_info.status == 1, channel_info.id == id).first()
        return record
    
    def get_all(self):
        record = session.query(channel_info).filter(channel_info.status == 1).all()
        return record
    
    def truncate_table(self):
        session.execute(text("DELETE FROM save_links"))
        session.commit()
        session.close()

session.close()
