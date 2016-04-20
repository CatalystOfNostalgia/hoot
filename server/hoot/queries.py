""" Use this file to interface with the database """
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
import models
from sqlalchemy import func

def insert_comment(item_id, relevancy, pleasantness, attention, \
                   sensitivity, aptitude, polarity):
    """ inserts an entry into the comments table """
    
    new_comment = models.comments.Comments( item_id = item_id, \
                                            relevancy = relevancy, \
                                            pleasantness = pleasantness, \
                                            attention = attention, \
                                            sensitivity = sensitivity, \
                                            aptitude = aptitude, \
                                            polarity = polarity)
    models.session.add(new_comment)
    models.session.commit()
                                          
def insert_media(title, creator, description, media_type, genre, asin):
    """ Inserts media into the database """
    new_media = models.multimedia.Multimedia( title = title, creator = creator,\
                                              description = description, \
                                              media_type = media_type, \
                                              genre = genre, \
                                              asin = asin )

    models.session.add(new_media)
    models.session.commit()

def insert_media_emotion(media_id, emotion):
    """ Adds an emotion to a media in the database """
    new_emotion = models.multimedia.MultimediaEmotions(media_id = media_id, \
                                                       emotion = emotion)

    models.session.add(new_emotion)
    models.session.commit()
                                                    

def find_media_by_asin(asin):
    """ Search the database by asin number """
    media = models.session.query(models.Multimedia).\
        filter(models.Multimedia.asin == asin).all()

    return media

def find_media_by_title(title):
    """ Search the database by title """
    media = models.session.query(models.Multimedia).\
        filter(models.Multimedia.title == title).all()

    return media

def find_media_by_creator(creator):
    """ Search the database by creator """
    media = models.session.query(models.Multimedia).\
        filter(models.Multimedia.creator == creator).all()

    return media

def find_comments_for_media(media_id):
    """ Find all comments associated with a media """
    comments = models.session.query(models.Comments).\
        filter(models.Comments.item_id == media_id).all()

    return comments

def rollback():
    """" Resets the SQLAlchemy session
    Use this if an exception is thrown or else you cannot make subsequent 
    queries
    """
    models.session.rollback()

