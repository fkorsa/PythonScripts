# Import all dependencies
import re, os, sys

def GetStringFromFilename(fileName, folder, parameters):
    """if (not '.dll' in fileName
        and not '.so' in fileName
        and not '.eon' in fileName
        ):
        raise ValueError()"""
    return '    <file>ui/wizard/' + os.path.basename(folder) + '/' + fileName + '</file>'

def ParseFiles(inputFolder, parameters):
    # Browse all files and subfolders
    for dirname, dirnames, filenames in os.walk(inputFolder):
        # Browse all files in current subfolder
        for filename in filenames:
            try:
                filenameString = GetStringFromFilename(filename, dirname, parameters)
                print(filenameString)
            except ValueError:
                print('Wrong filename. Skipping this file.')

if __name__ == "__main__":
    inputFolder = ''

    if len(sys.argv) < 2:
        inputFolder = input('>> Input folder : ')
    else:
        inputFolder = sys.argv[1]
    ParseFiles(inputFolder, ['', '', ''])