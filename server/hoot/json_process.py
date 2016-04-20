import json

"""
This script takes a comment in comment.txt and puts it in the json
stored in samples.json
"""

with open('samples.json', 'r') as f:
    samples = json.loads(f.read())

with open('comment.txt', 'r') as f:
    data = f.read().replace('\n', '')

samples['comments'].append(data)
with open('samples.json', 'w') as f:
    f.write(json.dumps(samples))



