# Import all dependencies
import re
import os
import sys

def GetNewName(oldName):
	if not oldName.startswith('_MG_'):
		raise ValueError()
	(basename, extension) = os.path.splitext(oldName)
	newFilename = re.sub(r'_MG_([0-9]*)', r'IMG_\1', basename) + extension
	return newFilename

folder = sys.argv[1]

# Browse all files and subfolders 
for dirname, dirnames, filenames in os.walk(folder):
	# Browse all files in current subfolder
	filenames.sort(reverse=True)
	for filename in filenames:
		try:
			newFilename = GetNewName(filename)
			if newFilename == filename:
				raise ValueError()
			print('renaming ' + dirname + '/' +  filename + ' into ' + folder + '/' + newFilename)
			os.rename(dirname + '/' + filename, folder + '/' + newFilename)
		except ValueError:
			print('Wrong filename. Skipping this file: ' + dirname + '/' + filename)