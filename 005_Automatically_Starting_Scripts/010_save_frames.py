# Usage:
#


# Import Needed Packages
from imutils.video import VideoStream
import argparse
import time
import cv2
import os


# Construct Argument Parser And Parse Arguments
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", required=True, help="Path To Output Directory")
ap.add_argument("-d", "--display", type=int, default=0, help="Display Frames (Bool)")
args = vars(ap.parse_args())


# Init Video Stream
print("[INFO] Warming Up Camera...")
vs = VideoStream(src=0).start()
# vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)

# Init Frame Count
count = 0


# Iterate Over Frames
while True:
	# Grab Frame
	frame = vs.read()
	
	# Write Current Frame To Output Directory
	imagePath = os.path.sep.join([args["output"], "{}.jpg".format(count)])
	cv2.imwrite(imagePath, frame)
	
	# Check If Display Flag Set
	if args["display"] > 0:
		# Show Output Frame
		cv2.imshow("Video Stream", frame)
		
		# Detect Keypress
		key == cv2.waitKey(1) & 0xFF
		
		# 'q' Pressed: Quit
		if key == ord("q"):
			break
			
	# Increment Count
	count += 1
	
	# If Count Reaches 100, Break Out Of Loop
	if count % 1000 = 0:
		break
		
		
# Cleanup
cv2.destroyAllWindows()
vs.stop()