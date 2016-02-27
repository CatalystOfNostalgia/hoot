from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy.dialects.mysql import Double
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class Comments(Base):
    __tablename__ = 'comments'

    comment_id      = Column(Integer, primary_key=True, \
                             autoIncrement=True, nullable=False)
    item_id         = Column(Integer, nullable=False)
    relevancy_score = Column(Integer, nullable=False)
    pleasantness    = Column(Double, nullable=False)
    attention       = Column(Double, nullable=False)
    sensitivity     = Column(Double, nullable=False)
    aptitude        = Column(Double, nullable=False)
    polarity        = Column(Double, nullable=False)
