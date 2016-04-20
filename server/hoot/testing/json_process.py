import json

with open('samples.json', 'r') as f:
    samples = json.loads(f.read())

with open('comment.txt', 'r') as f:
    data = f.read().replace('\n', '')

samples['comments'].append(data)
with open('samples.json', 'w') as f:
    f.write(json.dumps(samples))



