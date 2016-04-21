#! python3
import json, gzip, time, random, argparse, os.path, rdflib, queries
import xml.etree.ElementTree as ET
from datetime import datetime
from aws_module import push_to_S3, setup_product_api
from comment_processing import calculateVectorsForAllComments
# from summarize import get_summary

print("parsing the sentic graph")
f = open('../senticnet3.rdf.xml') # may need to adjust p
g = rdflib.Graph()
g.parse(f)
print("done parsing")

# just for counting the # of products posted to S3
i = 0

# for parsing the UCSD zipfiles
def parse(path, skip, amount, productapi, producttype):
    if skip is None:
        skip = 0
    if amount is None:
        # search until end of file
        amount = 999999999
    allReviews = gzip.open(path, 'r')
    # keep track of currrent product
    global i

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
                handleReview(current_asin, reviews_for_current_asin, productapi, producttype)
            reviews_for_current_asin = list()
            current_asin = review["asin"]

        reviews_for_current_asin.append(review)

# takes our constructed JSON file and runs our processing methods on it
def handleReview(asin, list_of_review_dicts, productapi, type):
    global i
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

    creator = "Unknown"
    image_node = item.find(namespace + "LargeImage")
    ean_node = item.find(namespace + "ItemAttributes").find(namespace + "EAN")
    title_node = item.find(namespace + "ItemAttributes").find(namespace + "Title")
    author_node = item.find(namespace + "ItemAttributes").find(namespace + "Author")
    director_node = item.find(namespace + "ItemAttributes").find(namespace + "Director")
    lead_actor_node = item.find(namespace + "ItemAttributes").find(namespace + "Actor")

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

    if author_node is not None:
        creator = author_node.text
    elif director_node is not None:
        creator = director_node.text
    elif lead_actor_node is not None:
        creator = lead_actor_node.text

    # add the creator to the dict
    product_dict["creator"] = creator

    # add the ASIN to the dict
    product_dict["asin"] = asin

    #TODO Insert the product into the database
    #insert_media(title, creator, description, media_type, asin)
    queries.insert_media(product_dict["title"], creator, product_dict["description"], producttype, asin)


    for review in list_of_review_dicts:
        comment_dict = dict()
        # if these dont exist in some of them, then so help me god
        comment_dict["rating"]  = review["overall"]
        comment_dict["helpful"] = review["helpful"]
        comment_dict["text"]    = review["reviewText"]
        product_dict["comments"].append(comment_dict)

    # now process this dict in comment_processing
    filename = product_dict["title"] + "$$$" + asin
    processed_dict = calculateVectorsForAllComments(product_dict, g)

    # create the summary
    processed_dict["summary"] = get_summary(processed_dict)

    processed_json = json.dumps(processed_dict, indent=4)

    ## TODO ADD EMOTION TO THE DATABASE
    print ("Adding product with asin: ", asin, "to S3 ---", i)
    push_to_S3(filename, processed_json)

# pass a list of the most relevant comment texts (above a relevancy threshold, or just the first 5)
def return_summary(product_dict):
    comments_to_get = 10    # return the first n comments
    comment_texts = list()
    top_comments = product_dict["comments"][:comments_to_get]
    for comment in top_comments:
        if comment["relevancy"] > 0.2:
            comment_texts.append(comment["text"])

    # if we don't get enough "good" comments, just return the first 5
    if len(comment_texts) < 5:
        comment_texts = list()
        for comment in top_comments[:5]:
            comment_texts.append(comment["text"])

    return get_summary(comment_texts)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Pass in UCSD review collection filename, amt of products to skip, and amt of products to upload')
    parser.add_argument('-f','--filename', help='filename of the UCSD review collection zip', required=True)
    parser.add_argument('-s','--skip', help='Skip the first n products in the set', required=False)
    parser.add_argument('-a', '--amount', help='The amount of products to process and upload to S3 / the database', required=False)
    parser.add_argument('-t', '--producttype', help='Enter the media type (Movie, TV, Books', required=True)
    args = vars(parser.parse_args())

    filename = args['filename']
    skip = args['skip']
    amount = args['amount']
    producttype = args['producttype']

    startTime = datetime.now()
    print ("starting")

    productapi = setup_product_api()

    parse(filename, skip, amount, productapi, producttype)

    print ("seconds taken: ",datetime.now() - startTime)