import sys
import os
import shutil

if len(sys.argv) != 3:
    print('Usage: [...].py 3ppFolder outputFolder')
    exit(1)

libFolder = sys.argv[1]
outputFolder = sys.argv[2]

if not os.path.isdir(libFolder):
    print(libFolder + ' is not a valid directory')
    exit(1)

if not os.path.isdir(outputFolder):
    print(outputFolder + ' is not a valid directory')
    exit(1)

excluded = ['qt', 'rhino', 'datakit', 'patchelf', 'cinema4d', 'quazip', 'ruby']

versions = {
    "csv": "2.1.0",
    "cuda_runtime": "11.0",
    "eigen": "3.3.7",
    "ffmpeg": "N-77953-gcc83177",
    "imgui": "1.82",
    "jwt-cpp": "0.4.0",
    "libzip": "1.8.0",
    "oidn": "1.0.0",
    "onetbb": "12.4",
    "openssl": "1.1.1o",
    "physx": "4.1",
    "resil": "1.8.2",
    "tbb": "2019-3",
    "zlib": "1.2.11"}

def getConanFile(name, version):
    if not version:
        if name not in versions:
            print(f'No version: {name}')
            version = '0.0.0'
        else:
            version = versions[name]
    return """from conan import ConanFile

class DerivedConanFile(ConanFile):
    name = "{name}"
    version = "{version}-r0"

    # Binary configuration
    settings = "os"
    
    # Sources are located in the same place as this recipe, copy them to the recipe
    exports_sources = "*.cmake", "include/*", "LICENSE", "version"

    def package(self):
        self.copy("*.cmake", excludes="test_package/*")
        self.copy("*", "include", "include")
        self.copy("LICENSE")
        self.copy("version")
        if self.settings.os == "Windows":
            self.copy(self.name + ".lib", "lib", "lib/win64")
        elif self.settings.os == "Macos":
            self.copy("lib" + self.name + ".a", "lib", "lib/mac64")
        elif self.settings.os == "Linux":
            self.copy("lib" + self.name + ".a", "lib", "lib/linux64")

    def package_info(self):
        self.cpp_info.libs = [self.name]

""".format(name=name, version=version)

def copypath(src, dst):
    if os.path.isfile(src):
        if not os.path.exists(dst):
            shutil.copy2(src, dst)
    else:
        shutil.copy2(src, dst)

def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore, dirs_exist_ok=True, copy_function=copypath)
        else:
            copypath(s, d)

def getSubFoldersOf(path):
    return [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]

def getSubFolderPathsOf(path):
    return [os.path.join(path, f) for f in getSubFoldersOf(path)]

def isValidLibraryPath(libraryPath):
    subFolders = getSubFoldersOf(libraryPath)
    for folder in subFolders:
        if folder.lower() == 'include' or folder.lower() == 'lib' or folder.lower() == 'bin':
            return True
    return False

def writeFile(path, contents):
    file = open(path, 'w')
    file.write(contents)
    file.close()

def treatLibraryVersion(name, version, path):
    if not isValidLibraryPath(path):
        print(f'ERROR: invalid library path {path}')
    else:
        outputPath = os.path.join(outputFolder, name)
        if version:
            outputPath = os.path.join(outputPath, version)
        os.makedirs(outputPath, exist_ok=True)
        copytree(path, outputPath)
        conanFileContents = getConanFile(name, version)
        writeFile(os.path.join(outputPath, 'conanfile.py'), conanFileContents)


def treatLibrary(libraryPath):
    name = os.path.basename(libraryPath)
    if name in excluded:
        return
    if isValidLibraryPath(libraryPath):
        treatLibraryVersion(name, '', libraryPath)
    else:
        for folder in getSubFoldersOf(libraryPath):
            treatLibraryVersion(name, folder, os.path.join(libraryPath, folder))

libraries = getSubFolderPathsOf(libFolder)

for library in libraries:
    treatLibrary(library)
