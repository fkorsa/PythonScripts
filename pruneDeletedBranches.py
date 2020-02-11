import subprocess
import os

def runCmd(cmd):
    print('Running ' + cmd + '...')
    output = subprocess.check_output(cmd)
    print(output)
    return output

runCmd('git status')