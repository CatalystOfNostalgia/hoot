from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class Book(Base):
    __tablename__  = 'book'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(256), nullable=False)
    author = Column(String(256), nullable=False)
