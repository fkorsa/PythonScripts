# Import all dependencies
import re, os, sys

file = open('deps.txt', 'r')
content = file.readlines()
file.close()

lastLib = ''
libList = []

for line in content:
	if line[0] != '\t':
		lastLib = line
	else:
		match = re.match(r'.*libstdc\+\+.*', line)
		if match != None:
			libList.append(lastLib)
			
for lib in libList:
	print lib