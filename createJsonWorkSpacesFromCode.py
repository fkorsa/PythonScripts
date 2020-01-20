import sys
import re
import json

if len(sys.argv) < 3:
    print('Usage: [...].py codefile outputJsonFile')

codeFile = sys.argv[1]
outputJsonFile = sys.argv[2]

file = open(codeFile, 'r')
code = file.read()
file.close()

pattern = r's\s*=\s*(("[^"]+"\s*)+);.*?DefaultWorkSpaceInfo\("(\w+)"_qs, tr\("(\w+)"\)'

hasMatch = False

workSpaces = dict()

for match in re.finditer(pattern, code, re.DOTALL | re.ASCII):
    hasMatch = True
    workSpace = dict()
    workSpace["data"] = "".join(match[1].split()).replace('"', '')
    workSpace["name"] = match[4]
    workSpaces[match[3]] = workSpace

if not hasMatch:
    print('Error: no match in the code file. Exiting.')
    exit(1)

with open(outputJsonFile, 'w') as outfile:
    json.dump(workSpaces, outfile, indent=2)
    print('Successfully written file ' + outputJsonFile)