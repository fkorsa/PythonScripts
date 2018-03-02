# Import all dependencies
import re, os, sys
from shutil import copyfile

inputFolder = input('>> Input folder : ')
outputFolder = input('>> Output folder : ')

if not os.path.exists(outputFolder):
    os.mkdir(outputFolder)

def GetNewName(oldName):
	"""if (not '.dll' in oldName 
		and not '.so' in oldName
		and not '.eon' in oldName
		):
		raise ValueError()"""
	newFilename = oldName
	newFilename = 'Logical' + newFilename
	return newFilename

# Browse all files and subfolders 
for dirname, dirnames, filenames in os.walk(inputFolder):
    # Browse all files in current subfolder
    filenames.sort(reverse=True)
    for filename in filenames:
        try:
            newFilename = GetNewName(filename)
            print('renaming ' + dirname + '/' +  filename + ' into ' + outputFolder + '/' + newFilename)
            copyfile(dirname + '/' + filename, outputFolder + '/' + newFilename)
        except ValueError:
            print('Wrong filename. Skipping this file.')