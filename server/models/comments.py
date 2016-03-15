from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy.dialects.mysql import DOUBLE
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class Comments(Base):
    __tablename__ = 'comments'

    comment_id      = Column(Integer, primary_key=True, \
                             autoincrement=True, nullable=False)
    item_id         = Column(Integer, nullable=False)
