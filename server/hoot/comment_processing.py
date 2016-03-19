#! python3
import sys
import nltk
from nltk.corpus import stopwords
from nltk import stem

import string
import json
import math

# currently uses my sampleText just as proof of concept
# eventually load json of product from AWS
# returns the JSON of the file, but with the vector space model included
def calculateVectorsForAllComments(productID):
    jsonfile = open("sampleText.json", 'r+')
    filetext = jsonfile.read()
    dictFromJSON = json.loads(filetext)

    tokenized_docs = buildListOfTokenizedDocuments(dictFromJSON)
    for comment in dictFromJSON["comments"]:
        # we dont want to calculate the vector every time
        if "vector_space" in comment:
            print("VSM already exists for this comment")
            continue

        comment["vector_space"] = calculateVector(tokenizeDocument(comment["text"]), tokenized_docs)

    return json.dumps(dictFromJSON)

# tokenize, stem, and remove stopwords from document
def tokenizeDocument(document):
    # remove punctuation (otherwise we have a bunch of empty tokens at the end)
    translate_table = dict((ord(char), None) for char in string.punctuation)
    document = document.translate(translate_table)
    # tokenize
    tokenized_doc = nltk.word_tokenize(document)
    # stem
    snowball = stem.snowball.EnglishStemmer()
    tokenized_doc = [snowball.stem(word) for word in tokenized_doc]
    # remove stop words
    tokenized_doc = [word for word in tokenized_doc if word not in stopwords.words('english')]
    return tokenized_doc

def buildListOfTokenizedDocuments(json_dict):
    tokenized_docs = []
    tokenized_docs.append(tokenizeDocument(json_dict["description"]))
    for comment in json_dict["comments"]:
        tokenized_docs.append(tokenizeDocument(comment["text"]))
    return tokenized_docs

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
        #print (numDocs ), " / ", getOccurencesOfToken(tokenized_docs, token)
        inverse_doc_freq = math.log( (1 + numDocs) / getOccurencesOfToken(tokenized_docs, token))
        vector_space_model[token] = (token_freq / inverse_doc_freq)
        # print (token," : ", (token_freq / inverse_doc_freq))
    return vector_space_model

if __name__ == '__main__':
    new_jsonfile = dictFromJSON = calculateRelevancyFromJSON("whatever we need to get the file from AWS")
    print(new_jsonfile)