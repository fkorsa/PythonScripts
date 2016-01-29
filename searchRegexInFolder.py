# Import all dependencies
import re, os, difflib, sys

# Get all the info from command line
sInputFolder = raw_input('>> Input folder : ')
sRegex = raw_input('>> Regex : ')
prog = re.compile(sRegex, re.DOTALL)

# Browse all files and subfolders 
for dirname, dirnames, filenames in os.walk(sInputFolder):
	# Browse all files in current subfolder
    for filename in filenames:
		
		# Open current file
		sParsedFile = os.path.join(dirname, filename)
		file = open(sParsedFile, 'r')
		sOldContents = file.read()
		file.seek(0)
		fileLines = file.readlines()
		file.close()
		print sParsedFile
		
		# Parse current file, and print all matches with home-made formatting
		for match in prog.finditer(sOldContents):
			# Retrieve the line number by counting the newlines before the match
			firstLine = sOldContents.count('\n', 0, match.start())
			# Retrieve the last line number by counting the newlines in the match
			lastLine = firstLine + sOldContents.count('\n', match.start(), match.end())
			if lastLine > firstLine and lastLine < len(fileLines):
				print 'Line ' + str(firstLine+1) + ' to line ' + str(lastLine+1) + ' :'
				if fileLines[firstLine:lastLine][-1] == '\n':
					print fileLines[firstLine:lastLine][0:-1]
				else:
					print fileLines[firstLine:lastLine]
				print 'Match : ' + match.group(0)
			elif firstLine < len(fileLines):
				print 'Line ' + str(firstLine+1) + ' :'
				if fileLines[firstLine][-1] == '\n':
					print fileLines[firstLine][0:-1]
				else:
					print fileLines[firstLine]
				print 'Match : ' + match.group(0)