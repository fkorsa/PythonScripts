import re
sContents = raw_input('>> String to parse : ')
sRegex = raw_input('>> Regex : ')
sReplace = raw_input('>> Replacement : ')
contents = re.sub(sRegex, sReplace, sContents)
print('Result : ' + contents)