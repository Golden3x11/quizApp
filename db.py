from sqlalchemy import create_engine, Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()


# classes to store rows fro database
class User(Base):
    __tablename__ = 'users'
    id = Column('idU', Integer, primary_key=True, autoincrement=True)
    login = Column('userlogin', String(255))
    password = Column('pswd', String(255))
    best_score = Column('bestScore', Integer, default=0)

    rank = relationship('Rank', backref='user')

    def __init__(self, login, password):
        self.login = login
        self.password = password


class Rank(Base):
    __tablename__ = 'ranking'
    id = Column('idR', Integer, primary_key=True, autoincrement=True)
    id_U = Column('idU', Integer, ForeignKey('users.idU'))
    date = Column('dateTime', DateTime, default=datetime.datetime.now())
    score = Column('score', Integer)

    def __init__(self, id_U, score):
        self.id_U = id_U
        self.score = score


# creating mysql engine, and connect to DB
# connection to local DB
engine = create_engine('mysql+pymysql://golden3x11:pass@127.0.0.1:3306/quizapp', pool_size=100)
Base.metadata.create_all(bind=engine)
