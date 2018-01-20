import csv
import sys

if len(sys.argv) < 3:
    print('Usage: script.py excelFile.csv outputFile.txt')
    exit(1)

outputFileContents = ''
csvDelimiter = '|'

with open(sys.argv[1], newline='') as csvfile:
    accountingRows = csv.reader(csvfile, delimiter=csvDelimiter)
    for row in accountingRows:
        currentColumn = 0
        date = ''
        description = ''
        category = ''
        value = ''
        who = ''
        onlyMe = ''
        onlyYou = ''

        for column in row:
            currentColumn = currentColumn + 1
            if currentColumn > 8:
                print('Error: too much columns in one row!')
                exit(1)
            if currentColumn == 1:
                dateFields = column.split('/')
                date = str(int(dateFields[2]) + 2000) + '\n' + str(int(dateFields[0]) - 1) + '\n' + dateFields[1]
            elif currentColumn == 2:
                description = column
            elif currentColumn == 3:
                category = column
            elif currentColumn == 4:
                value = column
            elif currentColumn == 5:
                if column == '1':
                    who = 'Flo'
                else:
                    who = 'Jess'
            elif currentColumn == 6:
                if column == '1' and who != 'Jess':
                    print('Warning: parse error. Bill attributed to both!')
                    print('Program will continue normally and attribute to Flo.')
            elif currentColumn == 7:
                if who == 'Flo':
                    onlyMe = column
                else:
                    onlyYou = column
            elif currentColumn == 8:
                if who == 'Jess':
                    onlyMe = column
                else:
                    onlyYou = column
            else:
                print('Error: wrong column index. Debug program.')
                exit(1)
        if onlyMe == '':
            onlyMe = '0.0'
        if onlyYou == '':
            onlyYou = '0.0'
        outputFileContents = outputFileContents + who + '\n' + date + '\n' + description + '\n' + category + '\n' + value + '\n' + onlyMe + '\n' + onlyYou + '\n'

with open(sys.argv[2], 'w') as outputFile:
    outputFile.write(outputFileContents)
    print('Successfully converted the file. Output:')
    print(sys.argv[2])
