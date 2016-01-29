# Import all dependencies
import re, os, difflib, sys, getopt

inputFolder = ''
outputFolder = ''
parsedFile = ''
createdFile = ''

isRegexFromFile = False
regexFile = ''

def readInput():
	global inputFolder
	global outputFolder
	global regex
	global replacement
	inputFolder = raw_input('>> Input folder : ')
	outputFolder = raw_input('>> Output folder : ')
	
def getFileContents(dirname, filename):
	global parsedFile
	parsedFile = os.path.join(dirname, filename)
	file = open(parsedFile, 'r')
	contents = file.read()
	file.close()
	return contents
	
def createParsedOutput(oldContents):
	global createdFile
	includeGuardMatch1 = re.match(r'#pragma once', oldContents)
	includeGuardMatch2 = re.match(r'#ifndef\w+?(.*?)\n.*?#define\w+?\1', oldContents)
	if includeGuardMatch1 == None and includeGuardMatch2 == None:
		outputFile = outputFolder + parsedFile[len(inputFolder):len(parsedFile)-len(filename)]
		if not os.path.exists(outputFile):
			os.mkdir(outputFile)
		createdFile = outputFolder + parsedFile[len(inputFolder):len(parsedFile)]
		file = open(createdFile, 'w')
		newContents = '#pragma once\n' + newContents
		file.write(newContents)
		file.close()

readInput()

# Browse all files and subfolders 
for dirname, dirnames, filenames in os.walk(inputFolder):
	# Browse all files in current subfolder
    for filename in filenames:
		oldContents = getFileContents(dirname, filename)
		createParsedOutput(oldContents)



