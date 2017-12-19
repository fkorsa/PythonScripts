def GetEntryMatchingBuildNumber(entries, buildNumber):
	showedTestIndex = -1
	if buildNumber >= len(entries) or entries[buildNumber]['bn'] != buildNumber:
		indexIt = len(entries) - 1
		while showedTestIndex == -1 and indexIt >= 0:
			if entries[indexIt]['bn'] == buildNumber:
				showedTestIndex = indexIt
			indexIt = indexIt - 1
	else:
		showedTestIndex = buildNumber
	return showedTestIndex

entries = [
		{'bn':3},
		{'bn':5},
		{'bn':1},
		{'bn':28},
		{'bn':2},
		]

for i in range(30):
	print(str(i) + ', ' + str(GetEntryMatchingBuildNumber(entries, i)) + ', ' + str(entries[GetEntryMatchingBuildNumber(entries, i)]))