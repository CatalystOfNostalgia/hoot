import sumy.parsers.plaintext
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

def get_summary(reviewList):
    linesMin = 200
    linesMax = 0
    for review in reviewList:
        lines = review.count('.') + review.count('!')+review.count('?')
        if lines >linesMax:
            linesMax = lines
        if lines < linesMin:
            linesMin = lines

    avgSize = linesMin + linesMax/2
    reviews = ' '.join(reviewList)
    parser = sumy.parsers.plaintext.PlaintextParser.from_string(reviews, Tokenizer("english"))
    stemmer = Stemmer("english")
    summarizer = LuhnSummarizer(stemmer)
    summary = summarizer(parser.document, 6)
    return summary
