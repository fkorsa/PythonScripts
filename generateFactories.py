import os
import sys
import shutil
import re
import fileUtils

inputFolder = sys.argv[1]


def capitalize(input):
    parts = input.split('_')
    capitalizedParts = []
    for part in parts:
        capitalizedParts.append(part[0].upper() + part[1:])
    return ''.join(capitalizedParts)


def toFileName(baseName, suffix):
    fileName = 'K'
    fileName += baseName
    fileName += suffix
    return fileName

class FileChanger(fileUtils.FileChanger):
    def __init__(self, snakeCaseName, capitalizedName):
        self.snakeCaseName = snakeCaseName
        self.capitalizedName = capitalizedName

    def changeContents(self, contents):
        snakeCaseName = self.snakeCaseName
        capitalizedName = self.capitalizedName
        if snakeCaseName in ['camera_switch_event', 'studio_switch_event']:
            contents = re.sub(r'KTimelineFlatPainter', 'KTimelineCirclePainter', contents)
        contents = re.sub(r'DAYARC', capitalizedName.upper(), contents)
        contents = re.sub(r'day_arc', snakeCaseName, contents)
        contents = re.sub(r'DAY_ARC', snakeCaseName.upper(), contents)
        contents = re.sub(r'DayArc', capitalizedName, contents)
        camelCaseName = capitalizedName[0].lower() + capitalizedName[1:]
        contents = re.sub(r'dayArc', camelCaseName, contents)
        return contents

suffixes = []
for _, _, filenames in os.walk(os.path.join(inputFolder, 'day_arc')):
    for filename in filenames:
        if filename.endswith('.cc'):
            suffixes.append(filename[7:-3])
        else:
            suffixes.append(filename[7:-2])
suffixes = set(suffixes)


def fillDirectory(dirname):
    for suffix in suffixes:
        snakeCaseName = 'day_arc'
        animationName = capitalize(snakeCaseName)
        baseName = toFileName(animationName, suffix)
        inputHeader = os.path.join(inputFolder, snakeCaseName, baseName + '.h')
        inputImpl = os.path.join(inputFolder, snakeCaseName, baseName + '.cc')
        animationName = capitalize(dirname)
        baseName = toFileName(animationName, suffix)

        headerPath = os.path.join(inputFolder, dirname, baseName + '.h')
        implPath = os.path.join(inputFolder, dirname, baseName + '.cc')

        shutil.copyfile(inputHeader, headerPath)
        shutil.copyfile(inputImpl, implPath)

        fileChanger = FileChanger(dirname, animationName)
        fileChanger.run(headerPath)
        fileChanger = FileChanger(dirname, animationName)
        fileChanger.run(implPath)

        print('  animation/types/' + dirname + '/' + baseName + '.h')
        print('  animation/types/' + dirname + '/' + baseName + '.cc')


for _, dirnames, filenames in os.walk(inputFolder):
    for dirname in dirnames:
        if dirname != 'day_arc':
            fillDirectory(dirname)
