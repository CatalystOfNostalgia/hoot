from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy.dialects.mysql import DOUBLE
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class Multimedia(Base):
    __tablename__ = 'multimedia_emotions'

    media_id     = Column(Integer, primary_key=True)
    pleasantness = Column(DOUBLE, nullable=False)
    attention    = Column(DOUBLE, nullable=False)
    sensitivity  = Column(DOUBLE, nullable=False)
    aptitude     = Column(DOUBLE, nullable=False)
    polarity     = Column(DOUBLE, nullable=False)
