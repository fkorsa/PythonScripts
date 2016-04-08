import json
import re

repo = 'Eon2016/Src'

VirtualPureRegexp = re.compile(r'(\s+)(=\s*0\s*;)')
AccoladesRegexp = re.compile(r'\s?{')

with open('overrideWarns.json', 'r') as f:
    W = json.loads(f.read())['inconsistent-missing-override']

for elem in W:
    linenumber = int(elem[1]) - 1
    try:
        with open(repo + elem[0], 'r') as f:
            alllines = f.read().split('\n')
            linesbefore = alllines[:linenumber]
            line = alllines[linenumber]
            linesafter = alllines[linenumber+1:]
    except :
        print 'Ignore read ' + str(elem)
        continue
    
    if 'EON_OVERRIDE' in line or 'GetNumberOfObjectsInObject' in line:
        print 'Ignore already EON_OVERRIDE ' + str(elem)
        continue
    
    if VirtualPureRegexp.search(line):
        line = VirtualPureRegexp.sub(r'\1EON_OVERRIDE\1\2', line, 1)
    elif '{' in line:
        line = AccoladesRegexp.sub(r'\tEON_OVERRIDE\t{', line, 1)
    else:
        line = line.replace(';', '\tEON_OVERRIDE;', 1)
    
    line = line.replace('virtual ', '', 1)
    line = line.replace('virtual\t', '', 1)
    line = line.replace('inline ', '', 1)
    line = line.replace('inline\t', '', 1)
    
    if 'EON_OVERRIDE' in line:
        with open(repo + elem[0], 'w') as f:
            f.write('\n'.join(linesbefore + [line] + linesafter).replace('/*virtual*/\t', '').replace('/*virtual*/ ', '').replace('/**/', ''))
    else:
        print 'No override in line ' + str(elem)
