import re
file = open('tobeparsed.txt', 'r')
contents = file.read()
contents = re.sub(r'(.*)\.(.*?)', r'\1~empty.\2', contents, 0, re.DOTALL)
#match = re.match(r'^[^;{]*?DoClone\([^;{]*?\)\s*(const)?\s*EON_OVERRIDE\s*(const)?(;|{)', contents, re.DOTALL)
#print match
#print match.group(0)
file.close()
file = open('parsed.txt', 'w')
file.write(contents)
file.close()