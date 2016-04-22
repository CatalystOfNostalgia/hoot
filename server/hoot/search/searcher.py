import json

from search.indexer import INDEX_DIR
from search.indexer import SCHEMA

from whoosh import index
from whoosh.query import Or
from whoosh.query import Term
from whoosh.qparser import QueryParser


def search(product_name=None, emotion=None):
    """
    Given product_name and emotion queries,
    returns the list of products that best match those queries.
    """
    ix = index.open_dir(INDEX_DIR)
    if product_name is None and emotion is None:
        return []
    elif product_name is None:
        return emotion_search(emotion, ix)
    elif emotion is None:
        return product_name_search(product_name, ix)

    return product_name_search(product_name, ix, emotion)


def emotion_search(emotion, ix):
    """
    Find all products that match the emotion.
    """
    qp = QueryParser('sentic_emotions', schema=SCHEMA)
    q = qp.parse(emotion)

    with ix.searcher() as s:
        results = s.search(q)
        products = build_json_from_results(results)

    qp = QueryParser('compound_emotions', schema=SCHEMA)
    q = qp.parse(emotion)

    with ix.searcher() as s:
        results = s.search()
        products.exten(build_json_from_results(results))

    return products


def product_name_search(product_name, ix, emotion=None):
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

        return build_json_from_results(results)


def build_json_from_results(results):
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
        result_dict['comments'] = json.loads(result['comments'])
        return_value.append(result_dict)

    return return_value


def convert_emotions_to_list(emotions):
    """
    Converts the space deliminated list of emotions to a python list.
    """
    return [emotion.capitalize() for emotion in emotions.split()]
