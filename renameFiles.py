# Import all dependencies
import re, os, sys
from shutil import copyfile

inputFolder = raw_input('>> Input folder : ')
outputFolder = raw_input('>> Output folder : ')

if not os.path.exists(outputFolder):
    os.mkdir(outputFolder)

def GetNewName(oldName):
	"""if (not '.dll' in oldName 
		and not '.so' in oldName
		and not '.eon' in oldName
		):
		raise ValueError()"""
	newFilename = oldName
	newFilename = newFilename + '_QT'
	newFilename = newFilename.replace('_WIN#', '')
	newFilename = newFilename.replace('_WIN', '')
	newFilename = newFilename.replace('_SPLIT', '')
	if not '.exe' in oldName:
		newFilename = 'lib' + newFilename
	newFilename = newFilename.replace('.exe', '')
	newFilename = newFilename.replace('.eon', '.so')
	#newFilename = re.sub(r'_([0-9]+)', r'_' + str(index), newFilename, 0, re.DOTALL)
	return newFilename

# Browse all files and subfolders 
for dirname, dirnames, filenames in os.walk(inputFolder):
    # Browse all files in current subfolder
    filenames.sort(reverse=True)
    for filename in filenames:
        try:
            newFilename = GetNewName(filename)
            print 'renaming ' + dirname + '/' +  filename + ' into ' + outputFolder + '/' + newFilename
            copyfile(dirname + '/' + filename, outputFolder + '/' + newFilename)
        except ValueError:
            print 'Wrong filename. Skipping this file.'