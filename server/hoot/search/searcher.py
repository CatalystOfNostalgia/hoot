import json

from search.indexer import INDEX_DIR
from search.indexer import SCHEMA

from whoosh import index
from whoosh.query import Or
from whoosh.query import Term
from whoosh.qparser import QueryParser

PAGE_LENGTH = 15


def search(product_name=None, emotion=None, page=1):
    """
    Given product_name and emotion queries,
    returns the list of products that best match those queries.
    """
    ix = index.open_dir(INDEX_DIR)

    if not page:
        page = 1

    if product_name is None and emotion is None:
        return []
    elif product_name is None:
        return emotion_search(emotion, ix, page)
    elif emotion is None:
        return product_name_search(product_name, ix, page)

    return product_name_search(product_name, ix, emotion, page)


def emotion_search(emotion, ix, page):
    """
    Find all products that match the emotion.
    """
    qp = QueryParser('sentic_emotions', schema=SCHEMA)
    q = qp.parse(emotion)

    products = []

    with ix.searcher() as s:
        results = s.search(q)
        products = build_json_from_results(results, page)

    qp = QueryParser('compound_emotions', schema=SCHEMA)
    q = qp.parse(emotion)

    with ix.searcher() as s:
        results = s.search(q)
        products.extend(build_json_from_results(results, page))

    return products


def product_name_search(product_name, ix, emotion=None, page):
    """
    Find all products that match the product_name.
    """
    qp = QueryParser('product_name', schema=SCHEMA)
    q = qp.parse(product_name)

    if emotion is not None:
        emotion_filter = Or(
            Term('sentic_emotions', emotion),
            Term('compound_emotions', emotion)
        )

    with ix.searcher() as s:
        if emotion is not None:
            results = s.search(q, filter=emotion_filter)
        else:
            results = s.search(q)

        return build_json_from_results(results, page)


def build_json_from_results(results, page):
    """
    Builds the JSON that will be returned from search. It will be a list
    of dictionaries that will be transformed into JSON.
    """
    return_value = []
    for result in results:
        result_dict = {}
        result_dict['product_name'] = result['product_name']
        result_dict['sentic_values'] = convert_emotions_to_list(result['sentic_emotions'])
        result_dict['compound_emotions'] = convert_emotions_to_list(result['compound_emotions'])
        result_dict['image_url'] = result['image_url']
        result_dict['sumy'] = result['sumy']
        result_dict['comments'] = paginate(json.loads(result['comments']), page)
        return_value.append(result_dict)

    return return_value


def convert_emotions_to_list(emotions):
    """
    Converts the space deliminated list of emotions to a python list.
    """
    return [emotion.capitalize() for emotion in emotions.split()]


def paginate(comments, page):
    """
    Gets the correct page of comments.
    """
    comment_length = len(coments)
    page_start = page * PAGE_LENGTH
    page_end = page * PAGE_LENGTH + PAGE_LENGTH

    if PAGE_LENGTH > comment_length:
        return comments
    elif page_end > comment_length:
        return comments[comment_length - PAGE_LENGTH:comment_length]
    else:
        return comments[page_start:page_end]
