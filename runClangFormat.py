import os
import sys
import fileUtils
import subprocess
import time

def runClangFormat(filePath):
    result = subprocess.run([os.environ['CLANG_FORMAT_PATH'], '-style=file', filePath], capture_output=True, text=True)
    result.check_returncode()
    fileUtils.writeFile(filePath, result.stdout)

def add(input):
    start = time.time()

    if os.path.isdir(input):
        for dirname, _, filenames in os.walk(input):
            for filename in filenames:
                if filename.endswith('.cs') or filename.endswith('.cpp'):
                    filePath = os.path.join(dirname, filename)
                    runClangFormat(filePath)
    else:
        runClangFormat(input)

    end = time.time()
    print('Duration: %.2f' % (end - start) + 's')

if __name__ == '__main__':
    add(sys.argv[1])
