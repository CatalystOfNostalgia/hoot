import sys
import string
import senticnet

# search for a concept given a certain string
def concept_search(query, start):
    f = open('concepts.txt', 'r')
    num = 0
    output = ''

    for line in f:
        if line.startswith(query):
            return (num, line.strip())

        num = num + 1

    return (-1, "NO CONCEPT")
            
# find all the concepts for a comment
def find_concepts(comment, start):
    words = comment.split()

    output = []

    for i in range(0, len(words)): 
        concept = words[i]
        last_concept = None
        line, found_concept = concept_search(words[i], start)
        j = i + 1

        if found_concept == concept:
            last_concept = found_concept

        while not line == -1 and j < len(words):
            concept = concept + '_' + words[j]
            j = j + 1
            line, found_concept = concept_search(concept, line)
            if found_concept == concept:
                last_concept = found_concept
        
        if last_concept != None:
            output.append(last_concept)
            
    if len(output) == 0:
        return "no concepts found"
    return output

def get_emotional_scores( concepts ):
    sn = senticnet.Senticnet()
    scores = {}

    for concept in concepts:
        scores[concept] = sn.concept(concept)

    return scores
    
def calculate_average( scores ):

    polarity_sum = 0

    average = {
        'pleasantness': 0,
        'attention'   : 0,
        'sensitivity' : 0,
        'aptitude'    : 0,
        'polarity'    : 0
    }

    for _, score in scores.iteritems():

        sentics = score['sentics']

        average['pleasantness'] = \
            average['pleasantness'] + (sentics['pleasantness'] * score['polarity'])

        average['attention'] = \
            average['attention'] + (sentics['attention'] * score['polarity'])

        average['sensitivity'] = \
            average['sensitivity'] + (sentics['sensitivity'] * score['polarity'])

        average['aptitude'] = \
            average['aptitude'] + (sentics['aptitude'] * score['polarity'])

        polarity_sum = polarity_sum + score['polarity']
    
    for emotion in average:
        if polarity_sum > 0:
            average[emotion] = average[emotion] / polarity_sum

    return average

def emotions ( comment ):
    comment.translate(string.maketrans("",""), string.punctuation)
    comment.lower()
    concepts = find_concepts(comment, 2)
    scores = get_emotional_scores(concepts)
    average = calculate_average(scores)
    return average

comment = "What has been said about the Dark Knight cannot be elaborated on - so I won't. The film is muscling its way into my #1 favorite comic movie adaptation of all time. The reason for my review is in hopes of saving you some money. This double disc Special Edition doesn't deliver the price you pay for it. There isn't even deleted scenes!!! I would save your very hard earned dollars and buy the single disc version and wait for the inevitable ULTIMATE re-release that will come later on down the road. But nonetheless, a great film - you will not be dissapointed; I just wish the studio would have given a better Special Edition release than what we have here. So enjoy!"

comment = comment.translate(string.maketrans("",""), string.punctuation)
comment = comment.lower()

average = emotions(comment)

print('average: \n' + str(average))

