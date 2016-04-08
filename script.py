import re
file = open('tobeparsed.txt', 'r')
contents = file.read()
contents = re.sub(r'^(\s*)(virtual\s*)?(([a-zA-Z_]+\s+)*?FlipControl\(.*?\)\s*?(const)?)(\s*(;|{))', r'\1\3 EON_OVERRIDE\6', contents, 0, re.DOTALL)
file.close()
file = open('parsed.txt', 'w')
file.write(contents)
file.close()