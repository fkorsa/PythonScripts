# Import all dependencies
import re, os, difflib, sys, getopt

inputFolder = ''
outputFolder = ''
regex = ''
replacement = ''
parsedFile = ''
createdFile = ''

isDiffEnabled = False
isRegexFromFile = False
regexFile = ''

def usage():
	print('Usage : python applyRegexToFolder.py [-d] [-r filename]')
	print('	-d : compute diff between the previous version and the parsed one')
	print('	-r filename : take the regex from the contents of a file, specified after the -r')

def parseOptions():
	global isDiffEnabled
	global isRegexFromFile
	global regexFile
	try:
		optlist, args = getopt.getopt(sys.argv[1:], 'dr:')
	except getopt.GetoptError as err:
		print str(err)
		usage()
		sys.exit(2)
	for option, value in optlist:
		if option == '-d':
			isDiffEnabled = True
		if option == '-r':
			isRegexFromFile = True
			regexFile = value

def readInput():
	global inputFolder
	global outputFolder
	global regex
	global replacement
	inputFolder = raw_input('>> Input folder : ')
	outputFolder = raw_input('>> Output folder : ')
	if not isRegexFromFile:
		regex = raw_input('>> Regex : ')
	else:
		file = open(regexFile, 'r')
		regex = file.read()
		file.close()
	replacement = raw_input('>> Replacement : ')
	
def getFileContents(dirname, filename):
	global parsedFile
	parsedFile = os.path.join(dirname, filename)
	file = open(parsedFile, 'r')
	contents = file.read()
	file.close()
	return contents
	
def createParsedOutput(oldContents):
	global createdFile
	newContents = re.sub(regex, replacement, oldContents)
	outputFile = outputFolder + parsedFile[len(inputFolder):len(parsedFile)-len(filename)]
	if not os.path.exists(outputFile):
		os.mkdir(outputFile)
	createdFile = outputFolder + parsedFile[len(inputFolder):len(parsedFile)]
	file = open(createdFile, 'w')
	file.write(newContents)
	file.close()
	return newContents
	
def computeDiff(oldContents, newContents):
	global createdFile
	differObject = difflib.Differ()
	sCompareOld = oldContents.splitlines(True)
	sCompareOld[len(sCompareOld)-1] += '\n'
	sCompareNew = newContents.splitlines(True)
	sCompareNew[len(sCompareNew)-1] += '\n'
	result = list(differObject.compare(sCompareOld, sCompareNew))
	file = open(createdFile + '.diff', 'w')
	file.write(parsedFile + ' -> ' + createdFile)
	file.writelines(result)
	file.close()

parseOptions()
readInput()

# Browse all files and subfolders 
for dirname, dirnames, filenames in os.walk(inputFolder):
	# Browse all files in current subfolder
    for filename in filenames:
		oldContents = getFileContents(dirname, filename)
		newContents = createParsedOutput(oldContents)
		if isDiffEnabled:
			computeDiff(oldContents, newContents)