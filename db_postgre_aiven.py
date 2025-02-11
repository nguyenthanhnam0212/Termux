import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, func, update, BigInteger, desc, text, Numeric, select, distinct
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import and_


load_dotenv()
engine = create_engine(os.getenv('POSTGRES_AIVEN') , echo = False)

Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class jav_censored(Base):
    __tablename__ = "jav_censored"
    id = Column(Integer, primary_key=True)
    file_id_photo = Column(String)
    file_id_video = Column(String)
    caption = Column(String)
    video_duration = Column(String)
    file_size = Column(Numeric(10, 2))
    vide_resolution = Column(String)
    note = Column(String)
    status = Column(Integer)
    __table_args__ = {'extend_existing': True}

class telegram_porn(Base):
    __tablename__ = "telegram_porn"
    id = Column(Integer, primary_key=True)
    file_id_photo = Column(String)
    file_id_video = Column(String)
    caption = Column(String)
    actor = Column(String)
    video_duration = Column(String)
    file_size = Column(Numeric(10, 2))
    vide_resolution = Column(String)
    nation = Column(String)
    note = Column(String)
    status = Column(Integer)
    __table_args__ = {'extend_existing': True}

Base.metadata.create_all(engine)

class check():
    
    def check_exist(id_movie, nation):
        regex_pattern = f'\\y{id_movie}\\y'
        exists = session.query(func.count()).filter(telegram_porn.status == 1, telegram_porn.nation == nation,
            telegram_porn.caption.op('~')(regex_pattern)
        ).scalar() > 0
        session.close()
        return exists
    
    def check_exist_cen(id_movie):
        regex_pattern = f'\\y{id_movie}\\y'
        exists = session.query(func.count()).filter(jav_censored.status == 1, 
            jav_censored.caption.op('~')(regex_pattern)
        ).scalar() > 0
        session.close()
        return exists
    
    def get_studio_cen():
        result = session.execute(select(distinct(jav_censored.note)).where(jav_censored.note.isnot(None))).scalars().all()
        return result

    def reset():
        session.rollback()
    
session.close()