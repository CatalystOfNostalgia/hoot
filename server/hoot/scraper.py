import sys, os, json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from amazon_scraper import AmazonScraper
import queries


class Scraper:
    #update all asins
    def update_reviews(asin):
        f = open(os.path.dirname(os.path.realpath(__file__)) + "/keys/aws_keys.json")
        configs = json.loads(f.read())
        amzn = AmazonScraper(configs["aws_public_key"], configs["aws_secret_key"], configs["product_api_tag"])
        p = amzn.lookup(ItemId=asin)
        reviews = p.reviews()
        dates = queries.find_date_for_review(asin)
        date = max(dates)
        update = False
        updateReviews = []
        for review in reviews:
            if date > review.date:
                update = True
        list_of_review_dicts =[]
        if(update):
             for review in reviews:
                 comment_dict = dict()
                 comment_dict["text"] = review.text
                 comment_dict
        return updateReviews
    #gets all asins and calls update
    def get_asins(self):
        media = queries.get_all_media()
        asins = []
        for item in media:
            asins.append(item.asin)
        for asin in asins:
            Scraper.update_reviews(asin)
