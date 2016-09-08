"""

author : fkorsakissok

description
Script only used to start the main script, which is compareThumbnails.py.
See the doc inside it for more details.

"""

import subprocess

def GetScriptFolder():
#
# returns the folder path of the currently running (or most recently ran) script
#
    Folder,junk = os.path.split(Child().GetCurrentScriptPath())
    return Folder

outputPath = os.path.join(GetScriptFolder(), 'output.png')

pythonProcess = subprocess.Popen(r'python compareThumbnails.py "' + outputPath + '"')
pythonProcess.wait()