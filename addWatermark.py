import os
import sys
from PIL import Image

sourceFolder = sys.argv[1]
destinationFolder = os.path.join(sourceFolder, 'watermark')
watermarkFile = sys.argv[2]

if not os.path.isfile(watermarkFile):
    print("The watermark file was not found: " + watermarkFile)
    exit(1)

downscaleResolutionX = 500
downscaleResolutionY = 600

def hasJpgExtension(filename):
    extension = os.path.splitext(filename)[1].lower()
    return extension == '.jpg' or extension == '.jpeg'


jpgFiles = [os.path.splitext(os.path.basename(filename))[0] for filename in os.listdir(sourceFolder) if
            os.path.isfile(os.path.join(sourceFolder, filename)) and hasJpgExtension(filename)]
print('Jpg files: ' + ', '.join(jpgFiles))

os.makedirs(destinationFolder, exist_ok=True)

watermarkImage = Image.open(watermarkFile)

for _, _, filenames in os.walk(sourceFolder):
    for filename in filenames:
        image = Image.open(os.path.join(sourceFolder, filename))
        downscaledImage = image.resize((downscaleResolutionX, downscaleResolutionY))
        position = (downscaleResolutionX - watermarkImage.size[0],
                    downscaleResolutionY - watermarkImage.size[1])
        downscaledImage.paste(watermarkImage, position, watermarkImage)
        downscaledImage.save(os.path.join(destinationFolder, filename))
    break
