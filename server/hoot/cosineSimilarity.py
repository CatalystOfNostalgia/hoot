__author__ = 'Anjana Rao'
import re,math, sys
from collections import Counter

WORD = re.compile(r'\w+')

def getCosine(text1, text2):
    vec1 = generateVector(text1)
    vec2 = generateVector(text2)

    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator)/denominator

def generateVector(text):
    words = WORD.findall(text)
    return Counter(words)

if __name__ == "__main__":
    cosine = getCosine(sys.argv[1], sys.argv[2])
    print(cosine)




