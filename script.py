import re
file = open('tobeparsed.txt', 'r')
contents = file.read()
contents = re.sub(r'Line [0-9]+:\s*', r'', contents, 0, re.DOTALL)
file.close()
file = open('parsed.txt', 'w')
file.write(contents)
file.close()