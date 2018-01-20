import csv
import sys

if len(sys.argv) < 3:
    print('Usage: script.py superBudgetFile.txt outputFile.csv')
    exit(1)

outputFileContents = ''
delimiter = '|'

with open(sys.argv[1], newline='') as superBudgetFile:
    currentRow = 0
    year = ''
    month = ''
    day = ''
    description = ''
    category = ''
    value = ''
    isFlo = ''
    isJess = ''
    onlyFlo = ''
    onlyJess = ''
    for row in superBudgetFile:
        currentRow = currentRow + 1
        row = row.replace('\n', '')
        row = row.replace('\r', '')
        if currentRow > 9:
            currentRow = 1

        if currentRow == 1:
            if row == 'Flo':
                isFlo = '1'
                isJess = ''
            else:
                isFlo = ''
                isJess = '1'
        elif currentRow == 2:
            year = str(int(row) - 2000)
        elif currentRow == 3:
            month = str(int(row) + 1)
        elif currentRow == 4:
            day = row
        elif currentRow == 5:
            description = row
        elif currentRow == 6:
            category = row
        elif currentRow == 7:
            value = row
        elif currentRow == 8:
            if isFlo == '1':
                onlyFlo = row
            else:
                onlyJess = row
        elif currentRow == 9:
            if isFlo == '1':
                onlyJess = row
            else:
                onlyFlo = row
        else:
            print('Error: wrong column index. Debug program.')
            exit(1)

        if currentRow == 9:
            if onlyFlo == '0.0':
                onlyFlo = ''
            if onlyJess == '0.0':
                onlyJess = ''
            outputFileContents = outputFileContents + month + '/' + day + '/' + year + delimiter
            outputFileContents = outputFileContents + description + delimiter
            outputFileContents = outputFileContents + category + delimiter
            outputFileContents = outputFileContents + value + delimiter
            outputFileContents = outputFileContents + isFlo + delimiter
            outputFileContents = outputFileContents + isJess + delimiter
            outputFileContents = outputFileContents + onlyFlo + delimiter
            outputFileContents = outputFileContents + onlyJess
            outputFileContents = outputFileContents + '\n'

with open(sys.argv[2], 'w') as outputFile:
    outputFile.write(outputFileContents)
    print('Successfully converted the file. Output:')
    print(sys.argv[2])
