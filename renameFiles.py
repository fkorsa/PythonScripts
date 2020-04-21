# Import all dependencies
import re, os, sys
from shutil import copyfile

def GetNewName(oldName, parameters):
    """if (not '.dll' in oldName
        and not '.so' in oldName
        and not '.eon' in oldName
        ):
        raise ValueError()"""
    pattern = r'([a-zA_Z_\.]+)([0-9]+)(.*)'
    beginning = re.sub(pattern, r'\1', oldName)
    pictureIndex = int(re.sub(pattern, r'\2', oldName)) - 1
    ending = re.sub(pattern, r'\3', oldName)
    pictureIndexString = str(pictureIndex)
    pictureIndexString = ('0' * (5 - len(pictureIndexString))) + pictureIndexString
    return beginning + pictureIndexString + ending

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