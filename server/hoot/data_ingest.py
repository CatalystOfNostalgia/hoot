#! python3
import json, gzip, time, bottlenose, random, boto, boto.s3.connection
from boto.s3.key import Key
from datetime import datetime
from urllib.error import HTTPError
import xml.etree.ElementTree as ET
from comment_processing import calculateVectorsForAllComments

s3conn = boto.connect_s3(aws_access_key_id = "AKIAIEMJ7S7X7VTJNMKQ",aws_secret_access_key = "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")
bucket = s3conn.get_bucket("hootproject")

def error_handler(err):
    ex = err['exception']
    if isinstance(ex, HTTPError) and ex.code == 503:
        time.sleep(random.expovariate(0.1))
        return True

def setupProductApi():
    public_key = "AKIAIEMJ7S7X7VTJNMKQ"
    secret_key = "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"
    tag = "hoot06-20"

    return bottlenose.Amazon(public_key, secret_key, tag, ErrorHandler=error_handler, MaxQPS=0.9)

def parse(path, productapi):
    g = gzip.open(path, 'r')
    # temporary, so i can break the loop early and not process every 6GB of review
    i = 0

    current_asin = "";
    reviews_for_current_asin = list()
    for l in g:
        # if (i >= 2): #6304994540
        #     break
        # i= i + 1
        review = json.loads(l.decode())
        # # if this is the first iteration of a new product, then set the current asin
        if (current_asin == ""):
            i= i + 1
            current_asin = review["asin"]
        # if we've reached a new set of reviews, process the set of previous reviews, keep track of current asin
        elif (current_asin != review["asin"]):
            handleReview(current_asin, reviews_for_current_asin, productapi, i)
            current_asin = review["asin"]
            i= i + 1
            reviews_for_current_asin = list()

        reviews_for_current_asin.append(review)
    print(i)


def handleReview(asin, list_of_review_dicts, productapi, i):
    print ("Adding product with asin: ", asin, "to S3 ---",i)
    product_dict = dict()
    product_dict["comments"] = list()

    # lookup product asin and parse XML for product description and metadata
    root = ET.fromstring(productapi.ItemLookup(ItemId=asin, ResponseGroup="EditorialReview,ItemAttributes"))
    namespace = root.tag[root.tag.find("{"): root.tag.find("}")+1]
    item = root.find(namespace + "Items").find(namespace + "Item")
    # if that doesnt work, this response is a bust. return
    if item is None:
        return
    if item.find(namespace + "ItemAttributes") is None:
        return
    ean_node = item.find(namespace + "ItemAttributes").find(namespace + "EAN")
    title_node = item.find(namespace + "ItemAttributes").find(namespace + "Title")

    # find the "best" desciption given for the product
    description = ""
    for child in root.findall(".//"+ namespace + "EditorialReview"):
        # this node should always exist, since if there was no content there would be no review
        review_node = child.find(namespace + "Content")
        review = ""
        if review_node is not None:
            review = review_node.text
        # I'm assuming that a longer editorial review will be better written / a synopsis of the product and its themes
        if ( len(review) > len(description) ):
            description = review

    if title_node is not None:
        product_dict["title"] = title_node.text
    if ean_node is not None:
        product_dict["ean"] = ean_node.text
    if len(description) > 0:
        product_dict["description"] = description

    for review in list_of_review_dicts:
        # product_dict["comments"] =
        comment_dict = dict()
        comment_dict["rating"]  = review["overall"]
        comment_dict["helpful"] = review["helpful"]
        comment_dict["text"]    = review["reviewText"]
        product_dict["comments"].append(comment_dict)

    # now process this dict in comment_processing
    filename = product_dict["title"] + "_" + asin
    calculateVectorsForAllComments(product_dict)
    #pushToS3(filename, calculateVectorsForAllComments(product_dict))

def pushToS3(filename, jsonToUpload):
    k = Key(bucket)
    k.key = filename
    k.set_contents_from_string(jsonToUpload)

if __name__ == '__main__':
    startTime = datetime.now()
    print ("starting")
    productapi = setupProductApi()

    parse("reviews_Movies_and_TV.json.gz", productapi)

    print("ending")
    print ("seconds: ",datetime.now() - startTime)