# Import all dependencies
import re, os, sys

contentsSum = ''
fileContents = ''

inputFolder = raw_input('>> Input folder : ')
outputFile = raw_input('>> Output file : ')
	
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
		contentsSum = contentsSum  + '<br/>' + filename + '<br/>' + fileContents
		
file = open(outputFile, 'w')
file.write(contentsSum)
file.close()