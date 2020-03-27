def readFile(filePath):
    file = open(filePath, 'r')
    contents = file.read()
    file.close()
    return contents

def writeFile(filePath, contents):
    file = open(filePath, 'w')
    file.write(contents)
    file.close()

class FileChanger:
    def run(self, filePath):
        contents = readFile(filePath)
        contents = self.changeContents(contents)
        writeFile(filePath, contents)

    def changeContents(self, contents):
        return contents