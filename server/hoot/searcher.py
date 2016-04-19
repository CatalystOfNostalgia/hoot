from indexer import INDEX_DIR
from indexer import SCHEMA

from whoosh import index
from whoosh import query
from whoosh.qparser import QueryParser


def search(product_name=None, emotion=None):
    """
    Given product_name and emotion queries,
    returns the list of products that best match those queries.
    """
    ix = index.open_dir(INDEX_DIR)
    if product_name is None and emotion is None:
        return {}
    elif product_name is None:
        return emotion_search(emotion, ix)
    elif emotion is None:
        return product_name_search(product_name, ix)

    return product_name_search(product_name, ix, emotion)


def emotion_search(emotion, ix):
    """
    Find all products that match the emotion.
    """
    qp = QueryParser('emotions', schema=SCHEMA)
    q = qp.parse(emotion)

    with ix.searcher() as s:
        results = s.search(q)
        return build_json_from_results(results)


def product_name_search(product_name, ix, emotion=None):
    """
    Find all products that match the product_name.
    """
    qp = QueryParser('product_name', schema=SCHEMA)
    q = qp.parse(product_name)

    if emotion is not None:
        emotion_filter = query.Term('emotions', emotion)

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
        result_dict['emotions'] = result['emotions']
        return_value.append(result_dict)

    return return_value


if __name__ == '__main__':
    print(search('title'))
    print(search(None, 'sadness'))
