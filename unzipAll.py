import zipfile
import sys
import os

inputFolder = sys.argv[1]
outputFolder = sys.argv[2]

from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir(inputFolder) if isfile(join(inputFolder, f))]

if not os.path.isdir(outputFolder):
	os.makedirs(outputFolder)

for fileName in onlyfiles:
	filePath = os.path.join(inputFolder, fileName)
	with zipfile.ZipFile(filePath, 'r') as zip_ref:
		print('Unzipping ' + filePath)
		zip_ref.extractall(outputFolder)
