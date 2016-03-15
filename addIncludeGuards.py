# Import all dependencies
import re, os, sys

inputFolder = ''
outputFolder = ''
parsedFile = ''
extension = '.rh'

def readInput():
	global inputFolder
	global outputFolder
	global extension
	inputFolder = raw_input('>> Input folder : ')
	outputFolder = raw_input('>> Output folder : ')
	extension = raw_input('>> File extension (in the form: ".cpp") : ')
	
def getFileContents(dirname, filename):
	global parsedFile
	parsedFile = os.path.join(dirname, filename)
	file = open(parsedFile, 'r')
	contents = file.read()
	file.close()
	return contents
	
def createParsedOutput(oldContents):
	includeGuardMatch1 = re.search(r'#pragma once', oldContents)
	includeGuardMatch2 = re.search(r'#ifndef\s+?(.*?)\n.*?#define\s+?\1', oldContents)
	newContents = ''
	if includeGuardMatch1 == None and includeGuardMatch2 == None:
		commentHeaderMatch = re.search(r'^\s*/\*.*?\*/', oldContents, re.DOTALL)
		if commentHeaderMatch:
			newContents = oldContents[:commentHeaderMatch.end()] + '\n#pragma once\n' + oldContents[commentHeaderMatch.end():]
		else:
			newContents = '#pragma once\n' + oldContents
	else:
		newContents = oldContents
	
	outputFile = outputFolder + parsedFile[len(inputFolder):len(parsedFile)-len(filename)]
	if not os.path.exists(outputFile):
		os.makedirs(outputFile)
	createdFile = outputFolder + parsedFile[len(inputFolder):len(parsedFile)]
	file = open(createdFile, 'w')
	file.write(newContents)
	file.close()

readInput()

# Browse all files and subfolders 
for dirname, dirnames, filenames in os.walk(inputFolder):
	# Browse all files in current subfolder
    for filename in filenames:
		if os.path.splitext(filename)[1] == extension:	
			oldContents = getFileContents(dirname, filename)
			createParsedOutput(oldContents)



