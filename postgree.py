import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, func, update, BigInteger, desc, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import and_


load_dotenv()
engine = create_engine(os.getenv('POSTGRES') , echo = False)

Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class save_links(Base):
    __tablename__ = "save_links"
    id = Column(Integer, primary_key=True)
    links = Column(String)
    username = Column(String)
    msgid = Column(Integer)
    target_channel = Column(BigInteger)
    media_type = Column(String)
    note = Column(String)
    status = Column(Integer)
    __table_args__ = {'extend_existing': True}

Base.metadata.create_all(engine)


class links_force():
    def __init__(self, links = None, username = None, msgid = None, target_channel = None, media_type = None, note = None, status = 1):
        self.links = links
        self.username = username
        self.msgid = msgid
        self.target_channel = target_channel
        self.media_type = media_type
        self.note = note
        self.status = status

    def save_to_links(self):
        sql = save_links(links = self.links, username = self.username, msgid = self.msgid, note = self.note, status = self.status)
        session.add(sql)
        session.commit()
        session.close()

    def update_links(self):
        session.query(save_links).filter(save_links.username == self.username).update({save_links.msgid: self.msgid})
        session.commit()
        session.close()

    def get_inf(self):
        record = session.query(save_links).filter(save_links.status == 1, save_links.username == self.username).first()
        return record
    
session.close()
