import json
import re

with open('warnings.txt', 'r') as f:
    w = json.loads(f.read())

for elem in w['missing-variable-declarations']:
    print elem[0] + ':' + elem[1] + '    ' + elem[3]

