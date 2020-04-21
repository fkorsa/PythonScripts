import os
import sys
import re
import fileUtils
import subprocess
import time

functionDeclPattern = re.compile(r'[a-zA-Z]+?\s*?::\s*?~?[a-zA-Z]+?\s*?\(')
commentPattern = re.compile(r'\s*?//\s*?\*+?')
commentLine = '// ' + ('*' * 97)


def runClangFormat(filePath):
    result = subprocess.run([os.environ['CLANG_FORMAT_PATH'], '-style=file', filePath], capture_output=True, text=True)
    result.check_returncode()
    fileUtils.writeFile(filePath, result.stdout)


def lineHasNamespaceBegin(line):
    namespaceIndex = line.find('namespace')
    if namespaceIndex > -1:
        commentIndex = line.find('//')
        usingIndex = line.find('using')
        isBeforeComment = commentIndex == -1 or namespaceIndex < commentIndex
        isBeforeUsing = usingIndex == -1 or namespaceIndex < usingIndex
        return isBeforeComment and isBeforeUsing
    return False


def braceBalance(line):
    opening = line.count('{')
    closing = line.count('}')
    balance = opening - closing
    if lineHasNamespaceBegin(line):
        balance -= 1
    return balance


class FileChanger(fileUtils.FileChanger):
    def changeContents(self, contents):
        lines = contents.split('\n')
        newContents = []
        lineIndex = 0
        currentBraceBalance = 0
        currentNamespaceBalance = 0
        isInFunctionDecl = False
        foundEndingWrapper = False
        for line in lines:
            addition = line
            currentBraceBalance += braceBalance(line)
            if lineHasNamespaceBegin(line):
                currentNamespaceBalance += 1
            if currentBraceBalance < 0:
                currentNamespaceBalance += currentBraceBalance
                currentBraceBalance = 0
            if not isInFunctionDecl and (currentBraceBalance == 0 or (
                    currentBraceBalance == 1 and braceBalance(line) == 1)) and '#include' not in line and 'using ' not in line and line.strip() != '':
                functionDeclMatch = functionDeclPattern.search(line)
                if functionDeclMatch is not None:
                    previousLine = lines[lineIndex - 1]
                    if commentPattern.match(previousLine) is not None:
                        newContents[-1] = commentLine + '\n'
                    elif previousLine.strip() == '':
                        newContents.append(commentLine + '\n')
                    else:
                        previousLine = lines[lineIndex - 2]
                        if commentPattern.match(previousLine) is not None:
                            newContents[-2] = commentLine + '\n'
                        elif previousLine.strip() == '':
                            newContents = newContents[:-2] + [commentLine + '\n'] + newContents[-2:]
                    isInFunctionDecl = True
                    foundEndingWrapper = False
            if isInFunctionDecl:
                if commentPattern.match(line) is not None:
                    addition = commentLine
                    foundEndingWrapper = True
                else:
                    braceIndex = line.find('{')
                    if braceIndex > -1:
                        isInFunctionDecl = False
                        if not foundEndingWrapper:
                            if braceIndex == 0:
                                if not foundEndingWrapper:
                                    newContents.append(commentLine + '\n')
                            else:
                                substringBeforeBrace = line[0:braceIndex]
                                if substringBeforeBrace.strip() == '':
                                    newContents.append(commentLine + '\n')
                                else:
                                    newContents.append(substringBeforeBrace + '\n' + commentLine + '\n')
                                addition = line[braceIndex:]
            if lineIndex < len(lines) - 1:
                addition += '\n'
            newContents.append(addition)
            lineIndex += 1
        return ''.join(newContents)


def treatFile(filePath):
    fileChanger = FileChanger()
    print('Processing ' + filePath)
    fileChanger.run(filePath)
    runClangFormat(filePath)

def add(input):
    start = time.time()

    if os.path.isdir(input):
        for dirname, _, filenames in os.walk(input):
            for filename in filenames:
                if filename.endswith('.cc'):
                    filePath = os.path.join(dirname, filename)
                    treatFile(filePath)
    else:
        treatFile(input)

    end = time.time()
    print('Duration: %.2f' % (end - start) + 's')


if __name__ == '__main__':
    add(sys.argv[1])
