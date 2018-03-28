import re
import os

inputFolder = input('>> Input folder : ')

contents = ''

# Browse all files and subfolders 
for dirname, dirnames, filenames in os.walk(inputFolder):
	# Browse all files in current subfolder
	for filename in filenames:
		contents += '<file>computer-modern/' + filename + '</file>\n'

file = open('parsed.txt', 'w')
file.write(contents)
file.close()