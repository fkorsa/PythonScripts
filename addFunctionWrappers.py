import os
import sys
import re
import fileUtils
import subprocess
import time

inputFolder = sys.argv[1]
start = time.time()

def runClangFormat(filePath):
    result = subprocess.run([os.environ['CLANG_FORMAT_PATH'], '-style=file', filePath], capture_output=True)
    result.check_returncode()


def braceBalance(fileContents, start, position):
    opening = fileContents.count('{', start, position)
    namespaces = fileContents.count('namespace', start, position)
    closing = fileContents.count('}', start, position)
    return opening - closing - namespaces


class FileChanger(fileUtils.FileChanger):
    def changeContents(self, contents):
        newContents = []
        lastIndex = 0
        lastPosition = 0
        currentBraceBalance = 0
        for match in re.finditer(
                r'\}?\s*(// ?\*+)?\s*(([a-zA-Z<>*_&: ]+)?\s+\*?\&?\*?\&?\w+::~?\w+\([^)]*\)\s*(const)?\s*(:\s*[^{/]+)?)\s*(// ?\*+)?\s*\{',
                contents):
            matchStart = match.start()
            if match.group(0)[0] == '}':
                matchStart += 1
            currentBraceBalance += braceBalance(contents, lastPosition, matchStart)
            lastPosition = matchStart
            if currentBraceBalance == 0:
                wrapper = '// ' + ('*' * 97)
                group = match.group(2).lstrip().rstrip()
                replacement = '\n\n' + wrapper + '\n' + group + '\n' + wrapper + '\n' + '{'
                newContents.append(contents[lastIndex:matchStart] + replacement)
                lastIndex = match.end()
        newContents.append(contents[lastIndex:])
        return ''.join(newContents)


for dirname, _, filenames in os.walk(inputFolder):
    for filename in filenames:
        if filename.endswith('.cc'):
            fileChanger = FileChanger()
            filePath = os.path.join(dirname, filename)
            print('Processing ' + filePath)
            fileChanger.run(filePath)
            runClangFormat(filePath)

end = time.time()
print('Duration: %.2f' % (end - start) + 's')