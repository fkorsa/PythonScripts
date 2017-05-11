# Import all dependencies
import re, os, sys

def getFileContents(parsedFile):
	file = open(parsedFile, 'r')
	contents = file.read()
	file.close()
	return contents
	
def createParsedOutput(oldContents, parsedFile):
	matchFound = False
	for match in re.finditer(r'<!--\s*(<FITLE>)', oldContents):
		matchFound = True
		newContents = oldContents[0:match.end(1)+1] + 'v_simu 2\n' + oldContents[match.end(1)+1:]
	if not matchFound:
		firstNewLineIndex = oldContents.find('\n')
		newContents = oldContents[0:firstNewLineIndex+1] + '<!--<FITLE>\nv_simu 2\n</FITLE>-->\n' + oldContents[firstNewLineIndex+1:]
	file = open(parsedFile, 'w')
	file.write(newContents)
	file.close()
	return newContents

if len(sys.argv) < 2:
	print 'Usage: python addSimuVersion.py absolutePathToFolder'
	raise SyntaxError('Wrong number of arguments.')

inputFolder = sys.argv[1]

# Browse all files and subfolders 
for dirname, dirnames, filenames in os.walk(inputFolder):
	# Browse all files in current subfolder
	for filename in filenames:
		garbage, extension = os.path.splitext(filename)
		if extension == '.svg':
			parsedFile = os.path.join(dirname, filename)
			print 'Processing ' + parsedFile
			oldContents = getFileContents(parsedFile)
			newContents = createParsedOutput(oldContents, parsedFile)