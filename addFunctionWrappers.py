import os
import sys
import re
import fileUtils
import subprocess

inputFolder = sys.argv[1]


def runClangFormat(filePath):
    result = subprocess.run([os.environ['CLANG_FORMAT_PATH'], '-style=file', filePath], capture_output=True)
    print('Running ' + ' '.join([os.environ['CLANG_FORMAT_PATH'], '-style=file', filePath]))
    result.check_returncode()


def isOutsideBody(fileContents, position):
    opening = fileContents.count('{', 0, position)
    namespaces = fileContents.count('namespace', 0, position)
    closing = fileContents.count('}', 0, position)
    return opening - closing - namespaces == 0


class FileChanger(fileUtils.FileChanger):
    def changeContents(self, contents):
        newContents = ''
        lastIndex = 0
        for match in re.finditer(
                r'\}?\s*(// ?\*+)?\s*(([a-zA-Z<>*_&: ]+)?\s+\w+::~?\w+\([^)]*\)\s*(const)?\s*(:\s*[^{/]+)?)\s*(// ?\*+)?\s*\{',
                contents):
            matchStart = match.start()
            if match.group(0)[0] == '}':
                matchStart += 1
            if isOutsideBody(contents, matchStart):
                wrapper = '// ' + ('*' * 97)
                group = match.group(2).lstrip().rstrip()
                replacement = '\n\n' + wrapper + '\n' + group + '\n' + wrapper + '\n' + '{'
                newContents = newContents + contents[lastIndex:matchStart] + replacement
                lastIndex = match.end()
        newContents = newContents + contents[lastIndex:]
        return newContents


for dirname, _, filenames in os.walk(inputFolder):
    for filename in filenames:
        if filename.endswith('.cc'):
            fileChanger = FileChanger()
            filePath = os.path.join(dirname, filename)
            print('Processing ' + filePath)
            fileChanger.run(filePath)
            runClangFormat(filePath)
