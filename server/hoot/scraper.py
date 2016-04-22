import sys, os, json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from amazon_scraper import AmazonScraper
import queries
import aws_module
import data_ingester

class Scraper:
    #update all asins
    def update_reviews(asin):
        f = open(os.path.dirname(os.path.realpath(__file__)) + "/keys/aws_keys.json")
        configs = json.loads(f.read())
        amzn = AmazonScraper(configs["aws_public_key"], configs["aws_secret_key"], configs["product_api_tag"])
        p = amzn.lookup(ItemId=asin)
        reviews = p.reviews()
        dates = queries.find_date_for_review(asin)
        media_type = queries.find_type_by_id(asin)
        date = max(dates)
        update = False
        for review in reviews:
            if date < int(review.date):
                update = True
        list_of_review_dicts =[]
        if(update):
             for review in reviews:
                 product_api = aws_module.setup_product_api()
                 comment_dict = dict()
                 comment_dict["text"] = review.text
                 comment_dict["unixtime"] = int(review.date)
                 list_of_review_dicts.append(comment_dict)
        return data_ingester.handleReview(asin, list_of_review_dicts, product_api, media_type)

    def get_asins(self):
        """
        gets all asins and calls update
        """
        media = queries.get_all_media()
        asins = []
        for item in media:
            asins.append(item.asin)
        for asin in asins:
            Scraper.update_reviews(asin)

if __name__ == '__main__':
    Scraper.get_asins()
