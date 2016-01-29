# Import all dependencies
import re, os, sys

linesNumber = 0
fileContents = ''

inputFolder = raw_input('>> Input folder : ')
	
def getFileContents(dirname, filename):
	parsedFile = os.path.join(dirname, filename)
	file = open(parsedFile, 'r')
	contents = file.read()
	file.close()
	return contents

# Browse all files and subfolders 
for dirname, dirnames, filenames in os.walk(inputFolder):
	# Browse all files in current subfolder
    for filename in filenames:
		fileContents = getFileContents(dirname, filename)
		linesNumber = linesNumber  + fileContents.count('\n') + 1
		
print linesNumber