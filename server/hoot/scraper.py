import sys, os, json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from amazon_scraper import AmazonScraper
from amazon import api
import calendar
from datetime import datetime
import queries
import time
import datetime
import url_scrape

#update all asins
def test_scrape(asin_list):
    f = open(os.path.dirname(os.path.realpath(__file__)) + "/keys/aws_keys.json")
    configs = json.loads(f.read())
    for asin in asin_list:
        amzn = AmazonScraper(configs["aws_public_key"], configs["aws_secret_key"], configs["product_api_tag"])
        p = amzn.lookup(ItemId=asin)
        reviews = p.reviews()
        all_reviews = list(reviews)
        for review in all_reviews:
            print(asin)
            print(review.url)
            d = review.date
            unix_time = calendar.timegm(d.utctimetuple())
            print(unix_time)
            print(url_scrape.parser(review.url))
            # for review in reviews:
            #     d = review.date
            #
            #     print(unix_time)
                #print(review.text)

if __name__ == '__main__':
   test_scrape(["0310893984","0740319116", "0766233995"])
    #Scraper.get_asins()


