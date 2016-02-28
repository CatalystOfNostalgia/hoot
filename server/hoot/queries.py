# use this file to interface with the database
import sys
sys.path.append('..')
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
                 sensitivity, aptitude, polarity, number_of_comments):

    new_media = models.multimedia.Multimedia( title = title, creator = creator,\
                                              description = description, \
                                              pleasantness = pleasantness, \
                                              attention = attention, \
                                              sensitivity = sensitivity, \
                                              aptitude = aptitude, \
                                              polarity = polarity, \
                                              number_of_comments = number_of_comments)

    models.session.add(new_media)
    models.session.commit()

# search for media by title
def find_media_by_title(title):
    media = models.session.query(models.Multimedia).filter(models.Multimedia.title == title)

    return media

# search for media by creator
def find_media_by_creator(creator):
    media = models.session.query(models.Multimedia).filter(models.Multimedia.creator == creator)

    return media

# find all the comments for a certain media
def find_comments_for_media(media_id):
    comments = models.session.query(models.Comments).filter(models.Comments.item_id == media_id)

    return comments

# rollbacks the sqlalchemy session, use if an exception occurs
def rollback():
    models.session.rollback()

insert_media('batman', 'anthony', 'so cool', .5, .5, .5, .5, .5, 0)
batman = find_media_by_title('batman')
print(batman)
