import re

file = open('override.txt', 'r')
contents = file.read()
file.close()
regex = r"(Vue/Source/.*?):([0-9]+):([0-9]+): warning: '(.*?)' overrides"
result = re.findall(regex, contents)
for elem in result:
    filename = elem[0]
    lineInFile = int(elem[1])
    characterInFile = elem[2]
    functionName = elem[3]
    file = open(filename, 'r')
    contents = file.read()
    file.close()
    currentLine = 1
    indexNewline = contents.find('\n')
    while(indexNewline > -1 and currentLine < lineInFile - 1):
        currentLine = currentLine + 1
        indexNewline = contents.find('\n', indexNewline + 1)
    startReplace = indexNewline + 1
    match = re.match(r'^[^;{]*?'+functionName+'\([^;{]*?\)\s*(const)?\s*EON_OVERRIDE\s*(const)?(;|{)', contents[startReplace:], re.DOTALL)
    if match == None:
        replacement = re.sub(r'^(\s*)(virtual\s*)?(([a-zA-Z_]+\s+)*?'+functionName+'\(.*?\)\s*?(const)?)(\s*(;|{))', r'\1\3 EON_OVERRIDE\6', contents[startReplace:], 1, re.DOTALL)
        contents = contents[:startReplace] + replacement
        file = open(filename, 'w')
        file.write(contents)
        file.close()
    else:
        print "function: " + functionName
        print "file: " + filename
        print "line: " + elem[1]
        print "Match:"
        print match.group(0)
        #raw_input('Press any key...')
        