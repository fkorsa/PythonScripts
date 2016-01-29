import re
file = open('tobeparsed.txt', 'r')
contents = file.read()
contents = re.sub(r'.*?extensionsTable\["\.([a-z]{3,4})"\].*?\n', r'\1\n', contents)
file.close()
file = open('parsed.txt', 'w')
file.write(contents)
file.close()