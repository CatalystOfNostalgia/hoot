#!/usr/bin/env python
import json
import os
import os.path

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir)

from aws_module import retrieve_from_S3
from queries import get_all_media
from queries import find_emotions_for_media
from queries import find_comment_count_for_media


from whoosh import index
from whoosh.fields import Schema
from whoosh.fields import TEXT
from whoosh.fields import KEYWORD
from whoosh.fields import NUMERIC
from whoosh.fields import STORED

INDEX_DIR = '/home/ubuntu/hoot/server/index'

SCHEMA = Schema(
    product_name=TEXT(stored=True),
    sentic_emotions=KEYWORD(stored=True, scorable=True),
    compound_emotions=KEYWORD(stored=True, scorable=True),
    comment_number=NUMERIC(sortable=True),
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
        try:
            s3_json = get_json_from_S3(product.title, product.asin)
        except:
            continue

        sentic_emotions = find_emotions_for_media(product.media_id)
        compound_emotions = s3_json['popular_compound_emotions']

        sentic_values_string = ' '.join([e for e in sentic_emotions])
        compound_emotions_string = ' '.join([e for e in compound_emotions])

        # trim comment dict
        comments = s3_json['comments']
        for comment in comments:
            comment.pop('vector_space')
            comment.pop('emotion_vector')
            comment['relevancy'] = float('%.2f' % comment['relevancy'])
            comment['sentic_emotions'] = [e.capitalize() for e in comment['sentic_emotions']]
            compound_emotions = []
            for e in comment['compound_emotions']:
                compound_emotions.append({
                    'compound_emotion': e['compound_emotion'].capitalize(),
                    'strength': e['strength'].capitalize()
                    })
            comment['compound_emotions'] = compound_emotions


        # write to indexer
        try:
            writer.add_document(
                product_name=product.title,
                sentic_emotions=sentic_values_string,
                compound_emotions=compound_emotions_string,
                comment_number=find_comment_count_for_media(product.media_id),
                image_url=s3_json['image_url'],
                sumy=s3_json['summary'],
                comments=json.dumps(comments),
            )
        except:
            print('ERROR with {}'.format(product.title))
            print(e)
        print('{} indexed'.format(product.title))

    writer.commit()


def get_json_from_S3(product_name, asin):
    """
    Retrieves the json file from s3.
    """
    filename = '{}$$${}'.format(product_name, asin)
    return json.loads(retrieve_from_S3(filename))


if __name__ == '__main__':
    indexer()
