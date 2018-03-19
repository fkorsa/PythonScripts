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
isDotMatchingAll = False
regexFile = ''

def usage():
	print('Usage : python applyRegexToFolder.py [-d] [-r filename]')
	print('	Copies all files inside the input folder into the output folder,')
	print('	and modified their contents by applying the given regex.')
	print('	-d : compute diff between the previous version and the parsed one')
	print('	-r filename : take the regex from the contents of a file, specified after the -r')

def parseOptions():
	global isDiffEnabled
	global isRegexFromFile
	global regexFile
	try:
		optlist, args = getopt.getopt(sys.argv[1:], 'dr:')
	except getopt.GetoptError as err:
		print(str(err))
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
	inputFolder = input('>> Input folder : ')
	outputFolder = input('>> Output folder : ')
	if not isRegexFromFile:
		regex = input('>> Regex : ')
	else:
		file = open(regexFile, 'r')
		regex = file.read()
		file.close()
	replacement = input('>> Replacement : ')
	
def getFileContents(dirname, filename):
	global parsedFile
	parsedFile = os.path.join(dirname, filename)
	try:
		file = open(parsedFile, 'r')
		contents = file.read()
		file.close()
	except UnicodeDecodeError:
		try:
			file = open(parsedFile, 'r', encoding='utf8')
			contents = file.read()
			file.close()
		except:
			print('Error while parsing file' + parsedFile)
	return contents
	
def createParsedOutput(oldContents, filename):
	global createdFile
	global isDotMatchingAll
	flags = 0
	if isDotMatchingAll:
		flags = re.DOTALL
	newContents = re.sub(regex, replacement, oldContents, flags=flags)
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

def setParameters(_inputFolder, _outputFolder, _regex, _replacement, _isDotMatchingAll):
	global inputFolder
	global outputFolder
	global regex
	global replacement
	global isDotMatchingAll
	
	inputFolder = _inputFolder
	outputFolder = _outputFolder
	regex = _regex
	replacement = _replacement
	isDotMatchingAll = _isDotMatchingAll

extFilter = None
def setExtensionFilter(_extFilter):
	global extFilter
	
	extFilter = _extFilter

def run():
	# Browse all files and subfolders 
	for dirname, dirnames, filenames in os.walk(inputFolder):
		# Browse all files in current subfolder
		for filename in filenames:
			if not extFilter or os.path.splitext(filename)[1][1:] in extFilter:
				oldContents = getFileContents(dirname, filename)
				newContents = createParsedOutput(oldContents, filename)
				if isDiffEnabled:
					computeDiff(oldContents, newContents)
			else:
				print('Ignored ' + os.path.join(dirname, filename))

parseOptions()

if __name__ == "__main__":
	readInput()
	run()