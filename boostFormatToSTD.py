import re, os

def boostToSTD(contents):
	output = re.sub(r'.*fmter ((% .*?)+);', r'\1', contents, 0, re.DOTALL)
	output = re.sub(r' *\n[ \t%]*', r'%', output)
	args = output.split('%')
	output = re.sub(r'.*?boost::w?format fmter\(L?"((\\?.)*)"\);.*', r'\1', contents, 0, re.DOTALL)
	spacing = re.sub(r'.*?boost::w?format fmter\(L?"((\\?.)*)"\);([\n \t]*)[^\n\t ]*?.*', r'\3', contents, 0, re.DOTALL)
	output2 = 'std::basic_ostringstream<TCHAR> sStream;' + spacing + 'sStream << _T("'
	i = 0
	argNb = 1
	while i < len(output):
		if output[i] == '%' and i < len(output)-2 and output[i+2] == '%':
			output2 += '") << ' + args[argNb] + ' << _T("'
			i = i + 3
			argNb = argNb + 1
		else:
			output2 += output[i]
			i = i + 1
	output2 += '");'
	ending = re.sub(r'.*?boost::w?format fmter\(L?"((\\?.)*)"\);.*?(\n[ \t]*[^\n]*?fmter.str\(\).*?;)', r'\3', contents, 0, re.DOTALL)
	ending = re.sub(r'fmter.str\(\)', r'sStream.str()', ending)
	return output2 + ending

def applyRegexToFile(filename, sOutFile):
	file = open(filename, 'r')
	fileContents = file.read()
	output = ''
	lastMatched = 0

	for match in list(re.finditer(r'boost::w?format fmter\(L?"(\\?.)*?"\);.*?fmter (% .*?)+;.*?fmter.str\(\).*?;', fileContents, re.DOTALL)):
		subStr = boostToSTD(fileContents[match.start():match.end()])
		output += fileContents[lastMatched:match.start()]
		output += subStr
		lastMatched = match.end()
	output += fileContents[lastMatched:]
	file.close()
	file = open(sOutFile, 'w')
	file.write(output)
	file.close()

sOutputFolder = 'test2'
sInputFolder = 'test'
for dirname, dirnames, filenames in os.walk(sInputFolder):
	
	# Browse all files in current subfolder
    for filename in filenames:
		
		# Retrieve the name of the current file
		sParsedFile = os.path.join(dirname, filename)
		
		# Compute the name of the file to create
		sPathToFile = sOutputFolder + sParsedFile[len(sInputFolder):len(sParsedFile)-len(filename)]
		if not os.path.exists(sPathToFile):
			os.mkdir(sPathToFile)
		sCreatedFile = sOutputFolder + sParsedFile[len(sInputFolder):len(sParsedFile)]
		# Parse current file
		applyRegexToFile(sParsedFile, sCreatedFile)