import os
import os.path

from emotion_processing.emotion import Emotion
from queries import get_all_media
from queries import find_emotions_for_media


from whoosh import index
from whoosh.fields import Schema
from whoosh.fields import TEXT
from whoosh.fields import KEYWORD
from whoosh.fields import STORED

INDEX_DIR = 'index'

SCHEMA = Schema(
    product_name=TEXT(stored=True),
    emotions=KEYWORD(stored=True, scorable=True),
    image_url=STORED,
    sumy=STORED,
    comments=STORED,
)


def indexer():
    if not os.path.exists(INDEX_DIR):
        os.mkdir(INDEX_DIR)

    ix = index.create_in(INDEX_DIR, SCHEMA)
    ix = index.open_dir('index')
    writer = ix.writer()

    products = get_all_media()
    for product in products:
        product_emotions = find_emotions_for_media(product.media_id)
        emotions_dict = {
            'pleasantness': product_emotions.pleasantness,
            'aptitude': product_emotions.aptitude,
            'attention': product_emotions.attention,
            'sensitivity': product_emotions.sensitivity,
        }
        # find the sentic values of the media
        emotion = Emotion(emotions_dict)
        sentic_values = emotion.get_all_sentic_values()
        sentic_values_string = ' '.join([value.name for value in sentic_values])
        # write to indexer
        writer.add_document(
            product_name=product.title,
            emotions=sentic_values_string,
            image_url=u'temp_url',
            sumy=u'temp_sumy',
            comments=u'temp_comments'
        )

    writer.commit()

    print('\n\nCONTENTS:')
    for doc in ix.searcher().documents():
        print(doc)


if __name__ == '__main__':
    indexer()
