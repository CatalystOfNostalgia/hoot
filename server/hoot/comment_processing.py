import nltk
import string
import json
import math
import collections

from nltk.corpus import stopwords
from nltk import stem
from emotion_processing.comment_emotions import emotions
from operator import itemgetter

# dictFromJSON: a dictionary from json.loads that follows our Product JSON structure
# adds relevancy rating (and eventually emotional rating) for all comments in the dict
# returns the modified dictionary
def calculateVectorsForAllComments(dictFromJSON, g):
    compound_emotion_dict = collections.defaultdict(int)

    if "description" not in dictFromJSON:
        calculateRelevancy = False
        return json.dumps(dictFromJSON, indent=4)

    processed_comments = list()

    compound_emotion_dict = collections.defaultdict(int)
    sentic_emotion_dict = collections.defaultdict(int)

    if "description" not in dictFromJSON:
        calculateRelevancy = False
        return json.dumps(dictFromJSON, indent=4)

    # TODO add the product to the DB here

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
        comment_emotion = emotions(comment["text"], g)
        comment["emotion_vector"] = comment_emotion.emotion_vector

        compound_emotions = comment_emotion.get_compound_emotion()
        sentic_values = comment_emotion.get_all_sentic_values()

        sentic_values = [value for value in sentic_values if value is not None]

        compound_emotions_list = []
        for compound_emotion, strength in compound_emotions:
            compound_emotions_list.append(
                {"compound_emotion": compound_emotion, "strength": strength}
            )
        comment["compound_emotions"] = compound_emotions_list

        ## CHANGE THIS TO USE A DICT TO PAIR KEY WITH VALUES
        sentic_dict = dict()
        for sentic in sentic_values:
            sentic_dict[sentic.name] = sentic.value
        comment["sentic_emotions"] = sentic_dict
        processed_comments.append(comment)

        # add all compound_emotions to the default dictFromJSON
        for compound in comment["compound_emotions"]:
            compound_emotion_dict[compound["compound_emotion"]] += 1

        # TODO: add the comment to the database

    # get max key from emotions
    dictFromJSON["max_compound_emotion"] = max(compound_emotion_dict, key=compound_emotion_dict.get)
    dictFromJSON["comments"] = sort_list_of_dicts(processed_comments)

    return dictFromJSON

def processFromAWS(productID):
    print("TODO")
    jsonfile = open("sampleText.json", 'r+')
    filetext = jsonfile.read()
    dictFromJSON = json.loads(filetext)
    calculateVectorsForAllComments(dictFromJSON)

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
