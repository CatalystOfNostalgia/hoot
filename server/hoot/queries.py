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
    models.session.add(new_comment)
    models.session.commit()
                                          
# inserts an entry into the multimedia table
def insert_media(title, creator, description, pleasantness, attention, \
                 sensitivity, aptitude, polarity, number_of_comments)

    new_media = models.multimedia.MultiMedia( title = title, creator = creator,\
                                              description = description, \
                                              pleasantness = pleasantness, \
                                              attention = attention, \
                                              sensitivity = sensitivity, \
                                              aptitude = aptitude, \
                                              polarity = polarity, \
                                              number_of_comments = number_of_comments)

    models.session.add(new_media)
    models.session.commit()
