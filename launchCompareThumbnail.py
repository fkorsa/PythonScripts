"""
author : fkorsakissok

description
Script only used to start the main script, which is compareThumbnail.py.
See the doc inside it for more details.

"""

def GetScriptFolder():
#
# returns the folder path of the currently running (or most recently ran) script
#
    Folder,junk = os.path.split(Child().GetCurrentScriptPath())
    return Folder

