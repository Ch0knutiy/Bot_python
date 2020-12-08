import requests
import json
r = requests.post('http://localhost:5005/model/parse',
                  json={'text': 'студент 89658242328'},
                  headers={'content-type': 'application/json'})
print(r.text)
r = requests.post('http://localhost:5005/model/parse',
                  json={'text': 'преподаватель'},
                  headers={'content-type': 'application/json'})
print(r.text)
