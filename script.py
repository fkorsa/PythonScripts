import re
file = open('tobeparsed.txt', 'r')
contents = file.read()
contents = re.sub(r'(.*?)return GetString\((.*?)\);(.*?\n)', r'\1layerName = std::move(GetString(\2));\3', contents)
file.close()
file = open('parsed.txt', 'w')
file.write(contents)
file.close()