#! python3
import json, gzip, time, bottlenose, random, boto, boto.s3.connection, argparse, os.path
from boto.s3.key import Key
from datetime import datetime
from urllib.error import HTTPError
import xml.etree.ElementTree as ET
from comment_processing import calculateVectorsForAllComments
from operator import itemgetter

# Load the AWS key information
f = open(os.path.dirname(os.path.realpath(__file__)) + "\keys\\aws_keys.json")
configs = json.loads(f.read())

s3conn = boto.connect_s3(aws_access_key_id=configs["aws_public_key"],aws_secret_access_key=configs["aws_secret_key"])
bucket = s3conn.get_bucket("hootproject")

def error_handler(err):
    ex = err['exception']
    if isinstance(ex, HTTPError) and ex.code == 503:
        time.sleep(random.expovariate(0.1))
        return True

def setupProductApi(public_key, secret_key, tag):
    return bottlenose.Amazon(public_key, secret_key, tag, ErrorHandler=error_handler, MaxQPS=0.9)

# for parsing the UCSD zipfiles
def parse(path, skip, amount, productapi):
    if skip is None:
        skip = 0
    if amount is None:
        # search until end of file
        amount = 999999999
    allReviews = gzip.open(path, 'r')
    # keep track of currrent product
    i = 0
    current_asin = "";
    reviews_for_current_asin = list()
    for reviewText in allReviews:
        review = json.loads(reviewText.decode())
        # # if this is the first iteration of a new product, then set the current asin
        if (current_asin == ""):
            current_asin = review["asin"]
        # if we've reached a new set of reviews, process the set of previous reviews, keep track of current asin
        elif (current_asin != review["asin"]):
            # products with < 5 comments really wont be that useful
            if len(reviews_for_current_asin) > 5:
                if (i < skip):
                    i = i + 1
                    continue

                i = i + 1
                # we only want to upload N times where N
                if (i > (skip + amount)):
                    break
                handleReview(current_asin, reviews_for_current_asin, productapi, i)
            reviews_for_current_asin = list()
            current_asin = review["asin"]

        reviews_for_current_asin.append(review)

# takes our constructed JSON file and runs our processing methods on it
def handleReview(asin, list_of_review_dicts, productapi, i):
    product_dict = dict()
    product_dict["comments"] = list()

    # lookup product asin and parse XML for product description and metadata
    root = ET.fromstring(productapi.ItemLookup(ItemId=asin, ResponseGroup="EditorialReview,ItemAttributes,Images"))
    namespace = root.tag[root.tag.find("{"): root.tag.find("}")+1]
    item = root.find(namespace + "Items").find(namespace + "Item")

    # if that doesnt work, this response is a bust. return
    if item is None:
        return
    if item.find(namespace + "ItemAttributes") is None:
        return
    ean_node = item.find(namespace + "ItemAttributes").find(namespace + "EAN")
    title_node = item.find(namespace + "ItemAttributes").find(namespace + "Title")
    image_node = item.find(namespace + "LargeImage")

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

    # check to see if these nodes actually exists, you never know
    if title_node is not None:
        product_dict["title"] = title_node.text
    if ean_node is not None:
        product_dict["ean"] = ean_node.text
    # we want the description to be substantial, some editorial reviews are garbage
    # anything below 30 characters will probably be not descriptive at all
    if len(description) > 30:
        product_dict["description"] = description
    else:
        # if we dont have a description we don't want anything to do with this
        return

    # Find the Image url
    # check to see if LargeImage, if not check Medium, if not that check Small
    if image_node is None:
        image_node = item.find(namespace + "MediumImage")
    if image_node is None:
        image_node = item.find(namespace + "SmallImage")

    if image_node is not None:
        image_url_node = image_node.find(namespace + "URL")
        if image_url_node is not None:
            # add the image url to the json
            product_dict["image_url"] = image_url_node.text
        else:
            product_dict["image_url"] = "None"

    for review in list_of_review_dicts:
        comment_dict = dict()
        # if these dont exist in some of them, then so help me god
        comment_dict["rating"]  = review["overall"]
        comment_dict["helpful"] = review["helpful"]
        comment_dict["text"]    = review["reviewText"]
        product_dict["comments"].append(comment_dict)

    # now process this dict in comment_processing
    filename = product_dict["title"] + "$$$" + asin
    processed_dict = calculateVectorsForAllComments(product_dict)
    processed_dict["comments"] = sortListOfDicts(processed_dict["comments"])
    processed_json = json.dumps(processed_dict, indent=4)

    ## TODO ADD IT TO THE DATABASE
    print ("Adding product with asin: ", asin, "to S3 ---", i)
    pushToS3(filename, processed_json)

def pushToS3(filename, jsonToUpload):
    k = Key(bucket)
    k.key = filename
    k.set_contents_from_string(jsonToUpload)

#
def sortListOfDicts(list_of_dicts):
    return sorted(list_of_dicts, key=itemgetter('relevancy'), reverse=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Pass in UCSD review collection filename, amt of products to skip, and amt of products to upload')
    parser.add_argument('-f','--filename', help='filename of the UCSD review collection zip', required=True)
    parser.add_argument('-s','--skip', help='Skip the first n products in the set', required=False)
    parser.add_argument('-a', '--amount', help='The amount of products to process and upload to S3 / the database', required=False)
    args = vars(parser.parse_args())

    filename = args['filename']
    skip = args['skip']
    amount = args['amount']

    startTime = datetime.now()
    print ("starting")

    productapi = setupProductApi(configs["aws_public_key"], configs["aws_secret_key"], configs["product_api_tag"])
    parse(filename, skip, amount, productapi)

    print ("seconds taken: ",datetime.now() - startTime)