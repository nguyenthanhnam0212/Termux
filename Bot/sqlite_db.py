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
    
session.close()


temp_db().truncate_temp()