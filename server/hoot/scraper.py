import sys, os, json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from amazon_scraper import AmazonScraper
import queries


class Scraper:
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
        if(update):
             for review in reviews:
                 updateReviews.append(review.text)
        return updateReviews
