import os
import shutil

mapFolder = r'C:\Work\Source\bound\Assets\Maps'
sceneFolder = r'C:\Work\Source\bound\Assets\Scenes'

isSceneMode = False

fileExtension = 'unity' if isSceneMode else 'tmx'
sourceFolder = sceneFolder if isSceneMode else mapFolder

class Range:
    x = 0
    y = 0

class DestinationMaps:
    start = Range()
    end = Range()

class Map:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getFileName(self):
        global sourceFolder
        global fileExtension
        return os.path.join(sourceFolder, 'map' + str(self.x) + '-' + str(self.y) + '.' + fileExtension)

    def isSame(self, otherMap):
        return self.x == otherMap.x and self.y == otherMap.y

sourceMap = Map(10, 10)

destinationMaps = DestinationMaps()
destinationMaps.start.x = 5
destinationMaps.start.y = 5
destinationMaps.end.x = 15
destinationMaps.end.y = 15

for x in range(destinationMaps.start.x, destinationMaps.end.x + 1):
    for y in range(destinationMaps.start.y, destinationMaps.end.y + 1):
        destinationMap = Map(x, y)
        if not sourceMap.isSame(destinationMap):
            shutil.copyfile(sourceMap.getFileName(), destinationMap.getFileName())