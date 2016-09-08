# Import all dependencies
import re, os, sys

inputFolder = raw_input('>> Input folder : ')
outputFolder = raw_input('>> Output folder : ')
inputFolder = inputFolder.replace('/', '\\')
outputFolder = outputFolder.replace('/', '\\')

# Browse all files and subfolders 
for dirname, dirnames, filenames in os.walk(inputFolder):
    # Browse all files in current subfolder
    for filename in filenames:
        fileExtension = re.sub(r'(.*)\.(.*?)', r'\2', filename, 0, re.DOTALL)
        if fileExtension == 'vob' or fileExtension == 'vue':
            dirname = dirname.replace('/', '\\')
            originalFile = dirname + '/' +  filename
            newFolder = dirname.replace(inputFolder, outputFolder)
            newFile = newFolder + '/' +  filename
            if not os.path.exists(newFolder):
                os.makedirs(newFolder)
            if os.path.exists(newFile):
                print 'not resaving ' + filename + ', because it already exists!'
            else:
                print 'saving ' + filename + '...'
                LoadObject(originalFile)
                SaveObject(newFile)
                Delete()