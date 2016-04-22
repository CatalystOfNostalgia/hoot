from BeautifulSoup import BeautifulSoup
import requests

def parser(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    review = [div.text for div in soup.findAll('div', attrs={'class': 'reviewText'})]
    return review
