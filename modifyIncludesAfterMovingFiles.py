import applyRegexToFolder as Apply

Apply.setExtensionFilter(['cpp', 'hpp', 'h', 'c'])

outputFolder = r'C:\Work\Source\composer3\src'
inputFile = r'C:\Work\Source\rename.log'

file = open(inputFile, 'r')
renameLog = file.readlines()
file.close()

renameLog = [x.strip() for x in renameLog] 

hasReadInitialFileName = False

renameFromString = 'rename from '
renameToString = 'rename to '

for line in renameLog:
	if line.startswith(renameFromString):
		initialFileName = line.replace(renameFromString, '')
		if initialFileName[-3:] == 'hpp':
			hasReadInitialFileName = True
			initialFileName = initialFileName.replace('src/', '')
	elif line.startswith(renameToString) and hasReadInitialFileName:
		hasReadInitialFileName = False
		newFileName = line.replace(renameToString, '')
		newFileName = newFileName.replace('src/', '')
		
		regex = r'#include\s+<' + initialFileName + '>'
		replacement = r'#include <' + newFileName + '>'
		print('replace ' + regex + ' with ' + replacement)
		Apply.setParameters(outputFolder, outputFolder, regex, replacement, _isDotMatchingAll=True, _silentMode=True)
		Apply.run()