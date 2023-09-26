import subprocess
import sys
import re
import os
import shutil


def modifySvgColor(svgFilePath):
    file = open(svgFilePath, 'r')
    contents = file.read()
    contents = re.sub(r'(<svg[^>]+style=")[^"]*?"', r'\1fill:#ffffff;fill-opacity:1;stroke:#ffffff;stroke-opacity:1"',
                      contents, 0, re.DOTALL)
    file.close()
    outputPath = r'C:/Users/flori/Downloads/tmp/' + os.path.basename(svgFilePath)
    file = open(outputPath, 'w')
    file.write(contents)
    file.close()
    return outputPath


inkscapePath = r"C:\Program Files\Inkscape\bin\inkscape.exe"


def exportSvg(filePath, outputPath):
    print('exporting ' + filePath + ' to ' + outputPath)
    modifiedPath = modifySvgColor(filePath)
    cmd = [inkscapePath, modifiedPath, '-w', '64', '-h', '64', '-o', outputPath]
    result = subprocess.run(cmd,
                            capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)


def parseFolder(inputFolder, outputFolder):
    shutil.rmtree(outputFolder, ignore_errors=True)
    os.mkdir(outputFolder)
    folderContents = os.listdir(inputFolder)
    for file in folderContents:
        filePath = os.path.join(inputFolder, file)
        if not os.path.isfile(filePath):
            continue
        exportSvg(filePath, os.path.join(outputFolder, os.path.splitext(file)[0] + '.png'))


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('Usage: python exportSvg.py inputFolder outputFolder')
        exit(1)
    parseFolder(sys.argv[1], sys.argv[2])
