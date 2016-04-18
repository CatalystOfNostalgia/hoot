import sys, os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import string
import emotion_processing.senticnet as senticnet

from emotion_processing.emotion import Emotion


def concept_search(query, start):
    """Search for a concept given a certain string."""
    f = open(os.path.abspath(os.path.dirname(__file__) + '/concepts.txt'), 'r')
    num = 0

    for line in f:
        if line.startswith(query):
            f.close()
            return (num, line.strip())

        num = num + 1

    f.close()

    return (-1, "NO CONCEPT")


def find_concepts(comment, start):
    """Find all the concepts for a comment."""
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

        if last_concept is not None:
            output.append(last_concept)
            sys.stdout.write('found: {}       \r'.format(last_concept))
            sys.stdout.flush()

    print('found {} concepts'.format(len(output)))
    return output


def get_emotional_scores(concepts, g):
    """ gets the emotional scores for concepts from the sentic database """

    sn = senticnet.Senticnet()
    scores = {}

    for concept in concepts:
        scores[concept] = sn.concept_local(concept, g)

    return scores


def calculate_average(scores):
    """Calculates the average emotion vector."""
    polarity_sum = 0

    average = {
        'pleasantness': 0,
        'attention': 0,
        'sensitivity': 0,
        'aptitude': 0,
        'polarity': 0
    }

    for _, score in scores.items():

        try:
            sentics = score['sentics']
        except KeyError:
            # Necessary since empty dicts are sometimes received
            continue

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


def emotions(comment, g):
    """
    Returns the emotion of the comment.

    In order to initialize g do the following:

        import rdflib

        f = open('senticnet3.rdf.xml') # may need to adjust path
        g = rdflib.Graph()
        g.parse(f)

    Initialize g in a place such that it will only be initialized once for
    all products/comments, since it takes ~1 minute to initilize.
    """
    comment = comment.translate(str.maketrans('', '', string.punctuation))
    comment = comment.lower()

    concepts = find_concepts(comment, 2)
    scores = get_emotional_scores(concepts, g)
    average = calculate_average(scores)
    return Emotion(average)
