import os
import codecs
import chardet

targetFormat = 'utf-8'

def convertFile(sourceFileName, targetFileName):
	with open(sourceFileName, 'rb') as sourceFileRaw:
		rawContents = sourceFileRaw.read()
		encoding = chardet.detect(rawContents)['encoding']
		with codecs.open(sourceFileName, 'r', encoding) as sourceFile:
			contents = sourceFile.read()
			writeConversion(contents, targetFileName)
			print('Done.')

def writeConversion(contents, targetFileName):
	with codecs.open(targetFileName, 'w', targetFormat) as targetFile:
		targetFile.write(contents)

def convertFileInPlace(sourceFileName):
	tmpFileName = sourceFileName + "-tmp"
	convertFile(sourceFileName, tmpFileName)
	os.remove(sourceFileName)
	os.rename(tmpFileName, sourceFileName)

inputFolder = input('>> Input folder : ')
for dirname, dirnames, filenames in os.walk(inputFolder):
	for filename in filenames:
		___, fileExtension = os.path.splitext(filename)
		fileExtension = fileExtension[1:]
		if fileExtension in ['cpp', 'h', 'hpp', 'qml', 'txt']:
			convertFileInPlace(os.path.join(dirname, filename))