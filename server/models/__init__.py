from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

db = create_engine('mysql+mysqldb://root:@localhost:8000/hoot')
db.echo = False

Session = sessionmake(bind=db)
session = Session()

# Import all models here

from multimedia import *
from comments import *
