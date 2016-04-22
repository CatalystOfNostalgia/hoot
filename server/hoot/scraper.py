import sys, os, json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from amazon_scraper import AmazonScraper
import url_scrape
import calendar
import queries
import time
import datetime
import data_ingester

def update_reviews(asin_list):
    for asin in asin_list:
        f = open(os.path.dirname(os.path.realpath(__file__)) + "/keys/aws_keys.json")
        configs = json.loads(f.read())
        amzn = AmazonScraper(configs["aws_public_key"], configs["aws_secret_key"], configs["product_api_tag"])
        p = amzn.lookup(ItemId=asin)
        reviews = p.reviews()
        dates = queries.find_date_for_review(asin)
        media_type = queries.find_type_by_id(asin)
        unix_dates = []
        for date in dates:
            unix_dates.append(get_date(date))
        date = max(unix_dates)
        update = False
        for review in reviews:
            if date < int(review.date):
                print("needs updating")
                update = True
        list_of_review_dicts =[]
        #if the product has new reviews get them from amazon
        if(update):
            all_reviews = list(reviews)
            for review in all_reviews:
                print(asin)
                print(review.url)
                d = review.date
                unix_time = calendar.timegm(d.utctimetuple())
                print(unix_time)
                print(url_scrape.parser(review.url))

                 # product_api = aws_module.setup_product_api()
                 # comment_dict = dict()
                 # comment_dict["text"] = review.text
                 # comment_dict["unixtime"] = int(review.date)
                 # list_of_review_dicts.append(comment_dict)
        #return data_ingester.handleReview(asin, list_of_review_dicts, product_api, media_type)

def get_date(d):
    unix_time = calendar.timegm(d.utctimetuple())
    return unix_time

def get_asins(self):
    """
    gets all asins and calls update
    """
    media = queries.get_all_media()
    asins = []
    for item in media:
        asins.append(item.asin)
    for asin in asins:
        update_reviews(asin)

# def test_scrape(asin):
#     f = open(os.path.dirname(os.path.realpath(__file__)) + "/keys/aws_keys.json")
#     configs = json.loads(f.read())
#     for asin in asin_list:
#         amzn = AmazonScraper(configs["aws_public_key"], configs["aws_secret_key"], configs["product_api_tag"])
#         p = amzn.lookup(ItemId=asin)
#         reviews = p.reviews()
#         all_reviews = list(reviews)
#         for review in all_reviews:
#             print(asin)
#             print(review.url)
#             d = review.date
#             unix_time = calendar.timegm(d.utctimetuple())
#             print(unix_time)
#             print(url_scrape.parser(review.url))
#         # for review in reviews:
#         #     d = review.date
#         #
#         #     print(unix_time)
#             #print(review.text)

if __name__ == '__main__':
    update_reviews(["0310893984","0740319116", "0766233995"])
    #Scraper.get_asins()


