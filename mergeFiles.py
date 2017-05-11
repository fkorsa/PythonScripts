import sys
if sys.argv[1] == "-i":
	linesFile = raw_input('>> File with the lines (1): ')
	removingFile = raw_input('>> File where we will be removing the lines present in (1) : ')
	keepingFile = raw_input('>> File where we will be keeping only the lines present in (1) : ')
	outputFile = raw_input('>> File to be created with the result : ')
else:
	linesFile = sys.argv[1]
	removingFile = sys.argv[2]
	keepingFile = sys.argv[3]
	outputFile = sys.argv[4]

with open(linesFile) as f:
	lines = f.readlines()

with open(removingFile) as f:
	linesWithRemoval = f.readlines()

with open(keepingFile) as f:
	linesWithKeeping = f.readlines()

newFileContent = ''
currentLine = 0
for line in lines:
	lineInt = int(line) - 1
	print 'currentLine: ' + str(currentLine)
	while currentLine < lineInt:
		if currentLine < len(linesWithRemoval):
			newFileContent = newFileContent + linesWithRemoval[currentLine]
		currentLine = currentLine + 1
	if currentLine < len(linesWithKeeping):
		newFileContent = newFileContent + linesWithKeeping[currentLine]
		currentLine = currentLine + 1
while currentLine < len(linesWithRemoval):
	newFileContent = newFileContent + linesWithRemoval[currentLine]
	currentLine = currentLine + 1

file = open(outputFile, 'w')
file.write(newFileContent)
file.close()