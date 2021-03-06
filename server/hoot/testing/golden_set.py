import json, rdflib, sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from emotion_processing.comment_emotions import emotions, ConceptError

with open('samples.json', 'r') as samples:
    data = json.loads(samples.read())

with open('../../senticnet3.rdf.xml', 'r') as f:
    print('spinning up db...')
    g = rdflib.Graph()
    g.parse(f)

for comment in data['comments']:
    try:
        emotion   = emotions(comment, g)
        sentics   = emotion.get_all_sentic_values()
        compounds = emotion.get_compound_emotion()

        print(comment[0:60])

        print('\temotion vector:')
        for emo in emotion.emotion_vector:
            print('\t\t{}: {}'.format(emo, emotion.emotion_vector[emo]))

        print('\tsentic values:')
        for sentic in sentics:
            if sentic is None:
                print('\t\tnone')
            else:
                print('\t\t{}'.format(sentic.name)) 

        print('\tcompound_emotion:')
        for compound, qualifier in compounds:
            print('\t\t{} {}'.format(qualifier.name, compound.name))
        
        print('\n')
    except ConceptError as e:
        print(e.value)
