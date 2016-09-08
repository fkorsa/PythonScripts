"""

author : fkorsakissok

description
Comparator for the automatic test that verifies the Windows Thumbnail handler.

It opens a file explorer window in a folder known to contain several types 
of files (.vue, .mat, .lrt etc.), then moves the window to a fixed place of the 
screen. Finally, it takes a screenshot at the location of the window.

"""

import platform, sys

outputFile = sys.argv[1]

if platform.system() == 'Windows':
	import win32ui, subprocess, os, time
	from PIL import ImageGrab

	# First, flush the thumbnail cache to be sure we are using the current thumbnail handler.
	os.system('taskkill /f /im explorer.exe')
	time.sleep(2)
	os.system(r'DEL /F /S /Q /A %LocalAppData%\Microsoft\Windows\Explorer\thumbcache_*.db')
	subprocess.Popen('explorer')

	# The path to the folder inside of which the thumbnail handler will be verified.
	picturePath = r'C:\test\Materials\Basic'

	# Get the leaf folder, which will be the title of the Explorer window.
	endFolder = os.path.split(picturePath)[1]

	# Open the Windows explorer
	subprocess.Popen('explorer.exe ' + picturePath)

	# Let it the time to setup, so that we can find it
	time.sleep(2)

	# Get a handle on the window that was just created, using its title 
	window = win32ui.FindWindow(None, endFolder)

	# Set its position, so that we're sure of its location
	windowLocation = (0, 0, 150, 1000)
	window.SetWindowPos(None, windowLocation, 0)

	# Bring it to the foreground, making sure the screenshot will capture this window
	window.SetForegroundWindow()

	# Let it the time to settle, because it will have to generate the thumbnails of all visible files
	time.sleep(5)

	# Actual screenshot time!
	screenshotLocation = (windowLocation[0] + 16, windowLocation[1] + 65, windowLocation[2] - 13, windowLocation[3] - 10)
	screenshot = ImageGrab.grab(screenshotLocation)
	screenshot.save(outputFile, 'png')

	os.system('taskkill /f /im explorer.exe')
	subprocess.Popen('explorer')
else:
	print 'Nothing to do here'
