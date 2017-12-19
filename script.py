import re
file = open('tobeparsed.txt', 'r')
contents = file.read()

###########################################
# Replace spanning on multiple lines
###########################################
#contents = re.sub(r'(.*?)', r'', contents, 0, re.DOTALL)

###########################################
# Replace spanning single line
###########################################
contents = re.sub(r'(.*\\)([^\\]+)', r'\1Default\\\2', contents)

###########################################
# Search spanning multiple lines
###########################################
#match = re.match(r'^[^;{]*?DoClone\([^;{]*?\)\s*(const)?\s*EON_OVERRIDE\s*(const)?(;|{)', contents, re.DOTALL)
#print match
#print match.group(0)



file.close()
file = open('parsed.txt', 'w')
file.write(contents)
file.close()