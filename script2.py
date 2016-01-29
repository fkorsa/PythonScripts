import re
file = open('tobeparsed.txt', 'r')
contents = file.read()
result = re.findall(r'[A-Z]+(?:_[A-Z]+)+', contents)
file.close()
s1 = set(result)

file = open('tobeparsed2.txt', 'r')
contents = file.read()
result = re.findall(r'[A-Z]+(?:_[A-Z]+)+', contents)
file.close()
s2 = set(result)

s = s2 - s1
print(s2 - s1)
file = open('parsed.txt', 'w')
file.write('\n'.join(s))
file.close()