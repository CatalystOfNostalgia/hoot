import sumy.parsers.plaintext
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.nlp.stemmers import Stemmer

def get_summary(reviewList):
    reviews = ' '.join(reviewList)
    parser = sumy.parsers.plaintext.PlaintextParser.from_string(reviews, Tokenizer("english"))
    stemmer = Stemmer("english")
    summarizer = LuhnSummarizer(stemmer)
    summary = summarizer(parser.document, 6)
    s = ""
    for sentence in summary:
        s+=str(sentence)
    return s
