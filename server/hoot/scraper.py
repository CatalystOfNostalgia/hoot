import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from amazon_scraper import AmazonScraper
import queries


class scraper:
    def update_reviews(asin):
        amzn = AmazonScraper("AKIAIEMJ7S7X7VTJNMKQ", "cV2hx5IEzshw71oPyJml7i+fG1aisZKbrmhuL0Ui", "hoot06-20")
        p = amzn.lookup(ItemId=asin)
        reviews = p.reviews()
        for review in reviews:
            print(review.date)


if __name__ == '__main__':
    scraper.update_reviews('B000GRFTPS')