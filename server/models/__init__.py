from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
import pymysql

db = create_engine('mysql+pymysql://root:@localhost:3306/hoot?charset=utf8')
db.echo = False

Session = sessionmaker(bind=db)
session = Session()

# Import all models here

from .multimedia import *
from .comments import *
from .multimedia_emotions import *
