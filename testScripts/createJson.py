import json

data = {'a': True,
     'b': 'Hello',
     'c': None}

with open('data.json', 'w') as f:
     json.dump(data, f)

with open('data.json', 'r') as f:
     data = json.load(f)
