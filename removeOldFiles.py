# This script is used to clean the cookbook from the old empty cockles that 
# should not be shipped with the product anymore. 
#
# It will search for a file named 'fileList.txt' in the current directory, and parse it.
# This file should contain the list of empty cockles to keep, in the following form:
#   Plants/Grasses - Plants|http://cornucopia3d.e-oncontent.com/storeItems/Plants/Grasses - Plants/RA_Weeds__Fields_and_Meadows_01_tpf_25_~~.tpf|20160506
# That is, 'folder|url|date'. The name of the file is mainly given by the url. The date is unused by this script.
#
# It will also ask you to give it the path to the input folder, which should be the root of the 
# cookbook repository. For example, "/c/work/cookbook", or just "./cookbook" (without the quotes, of course).
import re, os

inputFolder = input('>> Input folder : ')

file = open('fileList.txt', 'r')
contents = file.read()
file.close()

# Replace the input structure (that should be like 'folder|url|date') with the relative paths
# of the files in the cookbook
contents = re.sub(r'(.+?)\|.+?(\1.+?)\|.*?\n', r'\2\n', contents, 0, re.DOTALL)
files = contents.split('\n')

# Browse all files and subfolders 
for dirname, dirnames, filenames in os.walk(inputFolder):
    # Browse all files in current subfolder
    for filename in filenames:
        if "_~~" in filename:
            filenameSearched = filename.replace("_-_PHOBIA", "")
            filenameSearched = filenameSearched.replace("_-_PLACEHOLDER", "")
            filenameSearched = dirname + '/' + filenameSearched
            filenameSearched = filenameSearched.replace('\\', '/')
            filenameSearched = re.sub(r'.*?cookbook/.*?/(.*)', r'\1', filenameSearched, 0, re.DOTALL)
            if filenameSearched not in files:
                print('Removing ' + filenameSearched + '.')
                os.remove(dirname + '/' + filename)
            else:
                print('Not removing ' + filenameSearched + '.')