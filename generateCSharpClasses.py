import sys
import os

outputDir = sys.argv[1]
if not os.path.isdir(outputDir):
    print(f'Input argument: {outputDir} is not a valid directory.')
    exit(1)

def write_contents(fileName, contents):
    print(f'Writing to {fileName}')
    file = open(fileName, 'w')
    file.write(contents)
    file.close()

def generate_contents(index):
    contents = f"""
    using Godot;
using System;

public partial class MyScript{index} : Sprite2D{{
"""
    for i in range(1, 100):
        contents += f"void MyFunc{i}() {{ GD.Print({i}); }}"
    contents += "}"

    return contents

for i in range(1, 100):
    directory = os.path.join(outputDir, f'dir{i}')
    os.mkdir(directory)
    for j in range(1, 100):
        index = i * 100 + j
        contents = generate_contents(index)
        write_contents(os.path.join(directory, f'MyScript{index}.cs'), contents)
print('Finished')