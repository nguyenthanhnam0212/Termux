import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, func, update, BigInteger, desc, text, Numeric 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import and_


load_dotenv()
engine = create_engine(os.getenv('POSTGRES') , echo = False)

Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class channel_info(Base):
    __tablename__ = "channel_info"
    id = Column(Integer, primary_key=True)
    links = Column(String)
    username = Column(String)
    msgid = Column(Integer)
    msgid_end = Column(Integer)
    target_channel = Column(BigInteger)
    media_type = Column(String)
    note = Column(String)
    status = Column(Integer)
    __table_args__ = {'extend_existing': True}

Base.metadata.create_all(engine)

class channel:
    def __init__(self, id = None, links = None, username = None, msgid = None, msgid_end = None ,target_channel = None, media_type = None, note = None, status = 1):
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

    def truncate_table(self):
        session.execute(text("TRUNCATE TABLE channel_info RESTART IDENTITY CASCADE"))
        session.commit()
        session.close()

    def get_all(self):
        record = session.query(channel_info).filter(channel_info.status == 1).order_by(channel_info.id).all()
        return record
    
    def reset():
        session.rollback()

session.close()