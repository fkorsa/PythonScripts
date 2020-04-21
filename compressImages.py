import os
import sys
import shutil
from PIL import Image


def compressImages(inputPath, outputPath):
    shutil.rmtree(outputPath, ignore_errors=True)
    os.makedirs(outputPath, exist_ok=True)
    for _, dirnames, filenames in os.walk(inputPath):
        for fileName in filenames:
            inputFilePath = os.path.join(inputPath, fileName)
            outputFilePath = os.path.join(outputPath, fileName)
            print('Processing ' + inputFilePath)
            image = Image.open(inputFilePath)
            image.save(outputFilePath, "JPEG", quality=30)


if __name__ == '__main__':
    compressImages(sys.argv[1], sys.argv[2])
