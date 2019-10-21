import os
import sys

cr2Folder = sys.argv[1]

def hasJpgExtension(filename):
    extension = os.path.splitext(filename)[1].lower()
    return extension == '.jpg' or extension == '.jpeg'

jpgFolder = os.path.join(cr2Folder, 'JPEG')
jpgFiles = [os.path.splitext(os.path.basename(filename))[0] for filename in os.listdir(jpgFolder) if os.path.isfile(os.path.join(jpgFolder, filename)) and hasJpgExtension(filename)]
print('Jpg files: ' + ', '.join(jpgFiles))

for _, _, filenames in os.walk(cr2Folder):
    for filename in filenames:
        basenameWithoutExt = os.path.splitext(os.path.basename(filename))[0]
        if not basenameWithoutExt in jpgFiles:
            filePath = os.path.join(cr2Folder, filename)
            print('Removing ' + filePath)
            os.remove(filePath)
    break