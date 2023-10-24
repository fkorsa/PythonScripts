# Import all dependencies
import re, os, difflib, sys, getopt
import locale

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
silentMode = False

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
	contents = ''
	file = open(parsedFile, 'rb')
	contents = file.read()
	file.close()
	try:
		contents = contents.decode('utf-8')
	except UnicodeDecodeError:
		try:
			contents = contents.decode(locale.getpreferredencoding(False))
		except:
			print('Error while parsing file' + parsedFile)
			contents = ''
	return contents
	
def createParsedOutput(oldContents, filename):
	global createdFile
	global isDotMatchingAll
	flags = 0
	if isDotMatchingAll:
		flags = re.DOTALL
	newContents = re.sub(regex, replacement, oldContents, flags=flags)
	if newContents != oldContents:
		outputFile = outputFolder + parsedFile[len(inputFolder):len(parsedFile)-len(filename)]
		if not os.path.exists(outputFile):
			os.mkdir(outputFile)
		createdFile = outputFolder + parsedFile[len(inputFolder):len(parsedFile)]
		file = open(createdFile, 'wb')
		file.write(newContents.encode('utf-8'))
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

def setParameters(_inputFolder, _outputFolder, _regex, _replacement, _isDotMatchingAll, _silentMode = False):
	global inputFolder
	global outputFolder
	global regex
	global replacement
	global isDotMatchingAll
	global silentMode
	
	inputFolder = _inputFolder
	outputFolder = _outputFolder
	regex = _regex
	replacement = _replacement
	isDotMatchingAll = _isDotMatchingAll
	silentMode = _silentMode

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
				if oldContents != '':
					newContents = createParsedOutput(oldContents, filename)
					if not silentMode:
						print('Processed ' + os.path.join(dirname, filename))
					if isDiffEnabled:
						computeDiff(oldContents, newContents)
			elif not silentMode:
				print('Ignored ' + os.path.join(dirname, filename))

parseOptions()

if __name__ == "__main__":
	readInput()
	run()