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

class abyss(Base):
    __tablename__ = "abyss"
    id = Column(Integer, primary_key=True)
    movie_name_vi = Column(String)
    movie_name_en = Column(String)
    movie_image = Column(String)
    actor = Column(String)
    movie_code = Column(String)
    status = Column(Integer)
    __table_args__ = {'extend_existing': True}

Base.metadata.create_all(engine)

class _ABYSS:
    def __init__(self, id = None, movie_name_vi = None, movie_name_en = None, movie_image = None, actor = None, movie_code = None, status = 1):
        self.id = id
        self.movie_name_vi = movie_name_vi
        self.movie_name_en = movie_name_en
        self.movie_image = movie_image
        self.actor = actor
        self.movie_code = movie_code
        self.status = status

    def get_inf(self):
        record = session.query(abyss).filter(abyss.movie_code == self.movie_code, abyss.status == 1).first()
        return record
    
    def get_search():
        record = (
        session.query(abyss)
        .filter(
            abyss.status == 3
        )
        .all()
    )
        return record

    def update_status(self):
        session.query(abyss).filter(abyss.movie_code == self.movie_code).update({abyss.status: self.status})
        session.commit()
        session.close()
    
    def reset():
        session.rollback()

session.close()

X = _ABYSS.get_search()
result = []
for i in X:
    result.append({"ID": i.movie_code, "name_en": i.movie_name_en})
print(result)


