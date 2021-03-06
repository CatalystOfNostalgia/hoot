import nltk
import string
import html
import json
import math
import queries
import collections

from nltk.corpus import stopwords
from nltk import stem
from emotion_processing.comment_emotions import emotions
from operator import itemgetter
from emotion_processing.comment_emotions import ConceptError

class NoEmotionsFoundError(Exception):

    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

# dictFromJSON: a dictionary from json.loads that follows our Product JSON structure
# adds relevancy rating (and eventually emotional rating) for all comments in the dict
# returns the modified dictionary
def calculateVectorsForAllComments(dictFromJSON, g):
    compound_emotion_dict = collections.defaultdict(int)
    sentic_emotion_dict = collections.defaultdict(int)

    processed_comments = list()
    overall_rating = 0.0

    # the product model from the DB
    product = queries.find_media_by_asin(dictFromJSON["asin"])

    tokenized_docs = buildListOfTokenizedDocuments(dictFromJSON)
    for comment in dictFromJSON["comments"]:
        vectorized_comment = calculateVector(tokenizeDocument(comment["text"]), tokenized_docs)
        vectorized_desc = calculateVector(tokenizeDocument(dictFromJSON["description"]), tokenized_docs)
        comment["vector_space"] = vectorized_comment
        relevancy = getCosine(vectorized_comment, vectorized_desc)

        if relevancy < 0.15:
            continue

        comment["relevancy"] = relevancy

        # add emotional score
        try:
            comment_emotion = emotions(comment["text"], g)
        except ConceptError:
            print("Not enough concepts to do anything useful - skipping this product")
            continue

        comment["emotion_vector"] = comment_emotion.emotion_vector

        compound_emotions = comment_emotion.get_compound_emotion()
        sentic_values = comment_emotion.get_all_sentic_values()

        sentic_values = [value.name for value in sentic_values if value is not None]

        compound_emotions_list = []
        for compound_emotion, strength in compound_emotions:
            compound_emotions_list.append(
                {"compound_emotion": compound_emotion.name, "strength": strength.name}
            )
        comment["compound_emotions"] = compound_emotions_list

        comment["sentic_emotions"] = sentic_values

        # add all compound_emotions to the default dictFromJSON
        for compound in comment["compound_emotions"]:
            compound_emotion_dict[compound["compound_emotion"]] += 1

        for sentic in comment["sentic_emotions"]:
            sentic_emotion_dict[sentic] += 1

        overall_rating += float(comment["rating"])

        # add the comment to the database
        # insert_comment(item_id, relevancy, pleasantness, attention, sensitivity, aptitude, polarity, date)
        queries.insert_comment(product.media_id,
                                comment["unixtime"],
                                comment["relevancy"],
                                comment["emotion_vector"]["pleasantness"],
                                comment["emotion_vector"]["attention"],
                                comment["emotion_vector"]["sensitivity"],
                                comment["emotion_vector"]["aptitude"],
                                comment["emotion_vector"]["polarity"])

        comment["text"] = html.unescape(comment["text"])
        processed_comments.append(comment)

    popular_compound_emotions = []
    if len(compound_emotion_dict) == 0:
        raise NoEmotionsFoundError("No compound emotions found")

    for i in range(0, 3):
        popular_emotion = max(compound_emotion_dict, key=compound_emotion_dict.get)
        popular_compound_emotions.append(popular_emotion)
        compound_emotion_dict.pop(popular_emotion)

    popular_sentic_emotions = []
    if len(sentic_emotion_dict) == 0:
        raise NoEmotionsFoundError("No sentic emotions found")

    for i in range(0, 3):
        popular_sentic = max(sentic_emotion_dict, key=sentic_emotion_dict.get)
        popular_sentic_emotions.append(popular_sentic)
        sentic_emotion_dict.pop(popular_sentic)
        # add emotion to the database
        queries.insert_media_emotion(product.media_id, popular_sentic)

    dictFromJSON["popular_compound_emotions"] = popular_compound_emotions
    dictFromJSON["popular_sentic_emotions"] = popular_sentic_emotions

    if len(processed_comments) > 0:
        rating = overall_rating / len(processed_comments)
        rating = float("{0:.2f}".format(rating))
        dictFromJSON["overall_rating"] = rating

    dictFromJSON["comments"] = sort_list_of_dicts(processed_comments)

    # get rid of escaped html characters in description
    dictFromJSON["description"] = html.unescape(dictFromJSON["description"])

    return dictFromJSON

# tokenize, stem, and remove stopwords from document
def tokenizeDocument(document):
    # remove punctuation (otherwise we have a bunch of empty tokens at the end)
    translate_table = dict((ord(char), " ") for char in string.punctuation)
    document = document.translate(translate_table)
    # tokenize
    tokenized_doc = nltk.word_tokenize(document)
    # stem
    snowball = stem.snowball.EnglishStemmer()
    tokenized_doc = [snowball.stem(word) for word in tokenized_doc]
    # remove stop words
    tokenized_doc = [word for word in tokenized_doc if word not in stopwords.words('english')]
    return tokenized_doc

# given the dictionary, return an array of all the tokenized comments
def buildListOfTokenizedDocuments(json_dict):
    tokenized_docs = []
    tokenized_docs.append(tokenizeDocument(json_dict["description"]))
    for comment in json_dict["comments"]:
        tokenized_docs.append(tokenizeDocument(comment["text"]))
    return tokenized_docs

# get count of all documents that contain the given token
def getOccurencesOfToken(tokenized_docs, token):
    occurences = 0
    for document in tokenized_docs:
        if token in document:
            occurences += 1
    return occurences

# calculate term frequency.
# 1 + log(1 + number of occurences of t in the document)
def calculateVector(tokenized_comment, tokenized_docs):
    vector_space_model = dict()
    comment = " ".join(tokenized_comment)

    for token in tokenized_comment:
        token_freq = comment.count(token)
        token_freq = 0 if token_freq == 0 else 1 + math.log(1 + token_freq)

        # now we need to calculate the IDF
        numDocs = len(tokenized_docs)
        inverse_doc_freq = math.log( (1 + numDocs) / getOccurencesOfToken(tokenized_docs, token))
        vector_space_model[token] = (token_freq / inverse_doc_freq)

    return vector_space_model

def getCosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator)/float(denominator)

# used for sorting the comments by relevancy
def sort_list_of_dicts(list_of_dicts):
    return sorted(list_of_dicts, key=itemgetter('relevancy'), reverse=True)

if __name__ == '__main__':
    new_jsonfile = calculateVectorsForAllComments("whatever we need to get the file from AWS")
    print(new_jsonfile)