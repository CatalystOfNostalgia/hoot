import json
import os
import os.path

from aws_module import retrieve_from_S3
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
    sentic_emotions=KEYWORD(stored=True, scorable=True),
    compound_emotions=KEYWORD(stored=True, scorable=True),
    image_url=STORED,
    sumy=STORED,
    comments=STORED,
)


def indexer():
    """
    Indexes all search criteria.
    """
    if not os.path.exists(INDEX_DIR):
        os.mkdir(INDEX_DIR)

    ix = index.create_in(INDEX_DIR, SCHEMA)
    ix = index.open_dir('index')
    writer = ix.writer()

    products = get_all_media()
    for product in products:
        s3_json = get_json_from_S3(product.title, product.asin)

        sentic_emotions = find_emotions_for_media(product.media_id)
        compound_emotions = s3_json['compound_emotions']

        sentic_values_string = ' '.join([e for e in sentic_emotions])
        compound_emotions_string = ' '.join([e for e in compound_emotions])

        # trim comment dict
        comments = s3_json['comments']
        for comment in comments:
            comment.pop('vector_space')
            comment.pop('emotion_vector')
            comment['relevancy'] = float('%2.f' % comment['relevancy'])

        # write to indexer
        writer.add_document(
            product_name=product.title,
            sentic_emotions=sentic_values_string,
            compound_emotions=compound_emotions_string,
            image_url=s3_json['image_url'],
            sumy=s3_json['sumy'],
            comments=json.dumps(comments),
        )

    writer.commit()


def get_json_from_S3(product_name, asin):
    """
    Retrieves the json file from s3.
    """
    filename = '{}$$${}'.format(product_name, asin)
    return json.loads(retrieve_from_S3(filename))


if __name__ == '__main__':
    indexer()