import re, json

file = open('override.txt', 'r')
contents = file.read()
file.close()
result = json.loads(contents)['inconsistent-missing-override']
for elem in result:
    filename = '.' + elem[0]
    lineInFile = int(elem[1])
    characterInFile = elem[2]
    functionName = re.match(r"^\s*'(.*?)' overrides a member", elem[3], re.DOTALL).groups(1)[0]
    print "Function name: " + functionName
    raw_input('Press any key...')
    file = open(filename, 'r')
    contents = file.read()
    file.close()
    currentLine = 1
    indexNewline = contents.find('\n')
    while(indexNewline > -1 and currentLine < lineInFile - 1):
        currentLine = currentLine + 1
        indexNewline = contents.find('\n', indexNewline + 1)
    startReplace = indexNewline + 1
    match = re.match(r'^.*?'+functionName+'\([^;{]*?\)\s*(const)?\s*EON_OVERRIDE\s*(const)?(;|{)', contents[startReplace:], re.DOTALL)
    if match == None:
        replacement = re.sub(r'^(\s*)(virtual\s*)?(([a-zA-Z_]+\s+)*?'+functionName+'\(.*?\)\s*?(const)?)(\s*(;|{))', r'\1\3 EON_OVERRIDE\6', contents[startReplace:], 1, re.DOTALL)
        contents = contents[:startReplace] + replacement
        file = open(filename, 'w')
        file.write(contents)
        file.close()