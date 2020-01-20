import re
file = open('tobeparsed.txt', 'r')
contents = file.read()
file.close()

pattern = r'(("[^"]+"\s*)+)'

match = re.match(pattern, contents)

if not match:
    print('no match')
    exit(1)

contents = "".join(match[1].split()).replace('"', '')

file = open('parsed.txt', 'w')
file.write(contents)
file.close()