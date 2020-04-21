def capitalize(input):
    parts = input.split('_')
    capitalizedParts = []
    for part in parts:
        capitalizedParts.append(part[0].upper() + part[1:])
    return ''.join(capitalizedParts)

def toFileName(baseName, suffix):
    fileName = 'K'
    fileName += baseName
    fileName += suffix
    return fileName