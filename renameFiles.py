# Import all dependencies
import re, os, sys
from shutil import copyfile

def GetNewName(oldName, parameters):
    """if (not '.dll' in oldName
        and not '.so' in oldName
        and not '.eon' in oldName
        ):
        raise ValueError()"""
    newFilename = oldName
    pictureIndex = re.sub(parameters[0] + parameters[1] + r'\.([0-9]+)\.png', r'\1', oldName)
    newFilename = parameters[0] + '_' + ('0' * (5 - len(pictureIndex))) + str(pictureIndex) + parameters[2] + '.png'
    return newFilename

def renameFiles(inputFolder, outputFolder, parameters):
    if not os.path.exists(outputFolder):
        os.mkdir(outputFolder)

    # Browse all files and subfolders
    for dirname, dirnames, filenames in os.walk(inputFolder):
        # Browse all files in current subfolder
        filenames.sort(reverse=True)
        for filename in filenames:
            try:
                newFilename = GetNewName(filename, parameters)
                inputFile = os.path.join(dirname, filename)
                outputFile = os.path.join(outputFolder, newFilename)
                print('renaming ' + inputFile + ' into ' + outputFile)
                copyfile(inputFile, outputFile)
            except ValueError:
                print('Wrong filename. Skipping this file.')

if __name__ == "__main__":
    inputFolder = ''
    outputFolder = ''

    if len(sys.argv) < 3:
        inputFolder = input('>> Input folder : ')
        outputFolder = input('>> Output folder : ')
    else:
        inputFolder = sys.argv[1]
        outputFolder = sys.argv[2]
    renameFiles(inputFolder, outputFolder, ['', '', ''])