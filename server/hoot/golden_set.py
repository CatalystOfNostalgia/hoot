import json, rdflib
from emotion_processing.comment_emotions import emotions

with open('samples.json', 'r') as samples:
    data = json.loads(samples.read())

with open('../senticnet3.rdf.xml', 'r') as f:
    print('spinning up db...')
    g = rdflib.Graph()
    g.parse(f)

for comment in data['comments']:
   emotion = emotions(comment, g)
   print(comment[0:30])
   print('\tsentic values: {}'.format(emotion.get_all_sentic_values()))
   print('\tcompound_emotion: {}'.format(emotion.get_compound_emotion()))
