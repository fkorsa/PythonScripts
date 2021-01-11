from pydub import AudioSegment
import re, os, sys

def convertFile(inputFile, outputFile):
    if '.wav' not in inputFile:
        raise ValueError()
    music = AudioSegment.from_wav(inputFile)
    outputFolder = os.path.split(outputFile)[0]
    if not os.path.exists(outputFolder):
        os.mkdir(outputFolder)
    music.export(outputFile, format="mp3")

def convertFiles(inputFolder, outputFolder):
    if not os.path.exists(outputFolder):
        os.mkdir(outputFolder)

    for dirname, dirnames, filenames in os.walk(inputFolder):
        filenames.sort(reverse=True)
        for filename in filenames:
            try:
                inputFile = os.path.join(dirname, filename)
                outputFile = os.path.join(outputFolder, os.path.split(dirname)[1], filename.replace('.wav', '.mp3'))
                print('converting ' + inputFile + ' into ' + outputFile)
                convertFile(inputFile, outputFile)
            except ValueError:
                print('Wrong filename. Skipping this file.')


if __name__ == "__main__":
    inputFolder = ''
    outputFolder = ''

    if len(sys.argv) < 3:
        inputFolder = input('>> Input folder : ')
        outputFolder = input('>> Output folder : ')
    else:
        inputFolder = sys.argv[1]
        outputFolder = sys.argv[2]
    convertFiles(inputFolder, outputFolder)
