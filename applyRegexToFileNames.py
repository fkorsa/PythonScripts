# Import all dependencies
import re, os, sys, shutil

inputFolder = ''
outputFolder = ''
regex = ''
replacement = ''
parsedFile = ''

def readInput():
	global inputFolder
	global outputFolder
	global regex
	global replacement
	inputFolder = input('>> Input folder : ')
	outputFolder = input('>> Output folder : ')
	regex = input('>> Regex : ')
	replacement = input('>> Replacement : ')
	
def createParsedOutput(dirname, oldFilename):
	newFilename = re.sub(regex, replacement, oldFilename)
	oldFilePath = os.path.join(dirname, oldFilename)
	outputFileDir = outputFolder + dirname[len(inputFolder):]
	newFilePath = os.path.join(outputFileDir, newFilename)
	if not os.path.exists(outputFileDir):
		os.mkdir(outputFileDir)
	shutil.copyfile(oldFilePath, newFilePath)
	print(oldFilePath + '  --->  ' + newFilePath)
	
readInput()

# Browse all files and subfolders 
for dirname, dirnames, filenames in os.walk(inputFolder):
	# Browse all files in current subfolder
    for filename in filenames:
		createParsedOutput(dirname, filename)