# Import all dependencies
import re, os, sys, subprocess, shutil

if len(sys.argv) < 3:
    print('Usage: python script.py pathToTmutilResult pathToBackup [--dry-run]')
    exit(1)

dryRun = False
if len(sys.argv) > 3 and sys.argv[3] == '--dry-run':
    dryRun = True
    print('Performing a dry run.')

tmutilResultFile = open(sys.argv[1], 'r')
backupPath = sys.argv[2]
print('backupPath: ' + backupPath)
content = tmutilResultFile.readlines()
tmutilResultFile.close()

modifiedFiles = []
addedFiles = []
removedFiles = []

def removeItem(fileOrDirectory):
    if os.path.exists(fileOrDirectory):
        if os.path.isdir(fileOrDirectory):
            print('Removing directory ' + fileOrDirectory)
            shutil.rmtree(fileOrDirectory)
        else:
            print('Removing file ' + fileOrDirectory)
            os.remove(fileOrDirectory)

def removeFirstSlash(somePath):
    if somePath[0] == '/':
        somePath = somePath[1:]
    return somePath

def craftRestoreCommand(filePath):
    filePathWithoutFirstSlash = removeFirstSlash(filePath)
    return ['tmutil',  'restore', os.path.join(backupPath, filePathWithoutFirstSlash), filePath]

def extractPath(fileLine, outputList):
    currentPath = ''
    if fileLine.find(')') != -1:
        currentPath = re.sub(r'.*?\)\s+(.*?)\s*', r'\1', fileLine, 0, re.DOTALL)
    else:
        currentPath = re.sub(r'[\+\!-]\s+[^\s]+?\s+(.*?)\s*', r'\1', fileLine, 0, re.DOTALL)
    currentPath = currentPath.replace('\n', '')
    outputList.append(currentPath)

def restoreFileList(fileList):
    for filePath in fileList:
        if not dryRun:
            removeItem(filePath)
            print('Restoring ' + filePath + '...')
            restoreCommand = craftRestoreCommand(filePath)
            subprocess.call(restoreCommand)
        else:
            print('Would restore: ' + filePath)


isChangeOnTwoLines = False
for line in content:
    if line[0:10] == '----------':
        break
    currentPath = ''
    if line.find('(') != -1 and line.find(')') == -1:
        isChangeOnTwoLines = True
        continue
    if isChangeOnTwoLines:
        extractPath(line, modifiedFiles)
        isChangeOnTwoLines = False
        continue
    firstSymbol = line[0]
    if firstSymbol == '!':
        extractPath(line, modifiedFiles)
    elif firstSymbol == '+':
        extractPath(line, addedFiles)
    elif firstSymbol == '-':
        extractPath(line, removedFiles)


for addedFile in addedFiles:
    if not dryRun:
        removeItem(addedFile)
    else:
        print('Would remove: ' + addedFile)


restoreFileList(modifiedFiles)
restoreFileList(removedFiles)
