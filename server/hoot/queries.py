# use this file to interface with the database

import models
from sqlalchemy import func

# inserts an entry into the comments table
def insert_comment(item_id, relevancy, pleasentness, attention, \
                   sensitivity, aptitude, polarity):
    
    new_comment = models.comments.Comment( item_id = item_id, \
                                           relevancy_score = relevancy, \
                                           pleasantness = pleasantness, \
                                           attention = attention, \
                                           sensitivity = sensitivity, \
                                           aptitude = aptitude, \
                                           polarity = polarity)
    models.session.add(new_user)
    models.session.commit()
                                          

