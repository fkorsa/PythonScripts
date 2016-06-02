# Import all dependencies
import re, os, sys
from shutil import copyfile

inputFolder = raw_input('>> Input folder : ')
outputFolder = raw_input('>> Output folder : ')

if not os.path.exists(outputFolder):
    os.mkdir(outputFolder)

# Browse all files and subfolders 
for dirname, dirnames, filenames in os.walk(inputFolder):
    # Browse all files in current subfolder
    filenames.sort(reverse=True)
    for filename in filenames:
        try:
            index = int(re.sub(r'.+?_([0-9]+).*', r'\1', filename, 0, re.DOTALL))
            index = index + 1
            newFilename = re.sub(r'_([0-9]+)', r'_' + str(index), filename, 0, re.DOTALL)
            print 'renaming ' + dirname + '/' +  filename + ' into ' + outputFolder + '/' + newFilename
            copyfile(dirname + '/' + filename, outputFolder + '/' + newFilename)
        except ValueError:
            print 'Wrong filename. Skipping this file.'