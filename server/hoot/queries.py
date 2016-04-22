""" Use this file to interface with the database """
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
import models
from sqlalchemy import func


def insert_comment(item_id, date, relevancy, pleasantness, attention,
                   sensitivity, aptitude, polarity):
    """ inserts an entry into the comments table """
    new_comment = models.comments.Comments( item_id = item_id, \
                                            relevancy = relevancy, \
                                            pleasantness = pleasantness, \
                                            attention = attention, \
                                            sensitivity = sensitivity, \
                                            aptitude = aptitude, \
                                            polarity = polarity,\
                                            comment_date = date)
    models.session.add(new_comment)
    models.session.commit()

def insert_media(title, creator, description, media_type, asin, date):
    """ Inserts media into the database """
    new_media = models.multimedia.Multimedia( title = title, creator = creator,\
                                              description = description, \
                                              media_type = media_type, \
                                              asin = asin, \
                                              last_updated = date)
    models.session.add(new_media)
    models.session.commit()

def insert_media_emotion(media_id, emotion):
    """ Adds an emotion to a media in the database """
    new_emotion = models.multimedia_emotions\
                        .MultimediaEmotions(media_id = media_id, \
                                            emotion = emotion)

    models.session.add(new_emotion)
    models.session.commit()

def remove_media(asin):
    media = find_media_by_asin(asin)

    clean_media(media.media_id)
    models.session.delete(media)

def clean_media(media_id):
    """ removes all the associated comments and emotions for a media """
    media_emotions = find_emotions_for_media(media_id)
    media_comments = find_comments_for_media(media_id)

    for emotion in media_emotions:
        models.session.delete(emotion)

    for comment in media_comments:
        models.session.delete(comment)

    models.session.commit()

def update_media(media_id, date):
    """ updates the last_updated date for a piece of media """
    update = models.session.query(models.Multimedia).\
        filter(models.Multimedia.media_id == media_id).one()

    update.last_updated = date

    models.session.commit()

def get_all_media():
    """ returns all the media """
    return models.session.query(models.Multimedia).all()

def find_media_by_asin(asin):
    """ Search the database by asin number """
    media = models.session.query(models.Multimedia).\
        filter(models.Multimedia.asin == asin).one()

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

def find_comment_count_for_media(media_id):
    """ Finds number of comments associated with a media. """
    return models.session.query(models.Comments).filter(
        models.Comments.item_id == media_id).count()

def find_emotions_for_media(media_id):
    """ Finds all the emotions for a given media """
    media_emotions = models.session.query(models.MultimediaEmotions).\
                  filter(models.MultimediaEmotions.media_id == media_id).all()

    emotions = []

    for emotion in media_emotions:
        emotions.append(emotion.emotion)

    return emotions


def find_date_for_review(asin):
    media = find_media_by_asin(asin)
    item_id = media.media_id
    comments = find_comments_for_media(item_id)
    dates = []
    for comment in comments:
        dates.append(comment.comment_date)
    return dates

def find_type_by_id(asin):
    media = find_media_by_asin(asin)
    return media.type

def rollback():
    """" Resets the SQLAlchemy session
    Use this if an exception is thrown or else you cannot make subsequent
    queries
    """
    models.session.rollback()

