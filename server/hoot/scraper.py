import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from amazon_scraper import AmazonScraper
import queries


class Scraper:
    def update_reviews(asin):
        amzn = AmazonScraper("AKIAIEMJ7S7X7VTJNMKQ", "cV2hx5IEzshw71oPyJml7i+fG1aisZKbrmhuL0Ui", "hoot06-20")
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


if __name__ == '__main__':
    Scraper.update_reviews('B000GRFTPS')