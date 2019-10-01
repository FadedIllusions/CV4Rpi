# Usage:
# python 008_capture_timelapse_frames.py --output output/images --delay 2

# Note: Raspbian OS Has Time Lapse Feature Built Into The respistill Command Line Tool.


# Import Needed Packages
from imutils.video import VideoStream
from datetime import datetime
import argparse
import signal
import time
import cv2
import sys
import os


# Handle Keyboard Interrupt
def signal_handler(sig, frame):
	print("[INFO] 'ctrl+c' Pressed. Pictures Saved In Specified Directory...")
	sys.exit(0)

	
# Construct Argument Parser And Parse Arguments
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", required=True, help="Path To Output Directory")
ap.add_argument("-d", "--delay", type=float, default=5.0, help="Delay (In Secs) Between Captures")
ap.add_argument("-dp", "--display", type=int, default=0, help="Should Frames Be Displayed (Bool)")
args = vars(ap.parse_args())


# Init Output Dir Path, Create Dir
outputDir = os.path.join(args["output"], datetime.now().strftime("%Y-%m-%d-%H%M"))
os.makedirs(outputDir)


# Init Video Stream
print("[INFO] Warming Camera Sensor...")
vs = VideoStream(src=0).start()
# vs = VideoStream(usePiCamera=True, resolution=(1920,1280), framerate=30).start()
time.sleep(2.0)

# Init Frame Count
count = 0

# Signal Trap To Handle Keyboard Interrupt
signal.signal(signal.SIGINT, signal_handler)
print("[INFO] Press 'ctrl+c' To Exit, Or 'q' To Quit If Display Option On...")


# Iterate Over Video Stream
while True:
	# Grab Frame
	frame = vs.read()
	
	# Draw Timestamp
	ts = datetime.now().strftime("%A %d %B %Y %I:%M:%S%p")
	cv2.putText(frame, ts, (10,frame.shape[0]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0,0,255), 1)
	
	# Write Current Frame To Output Directory
	filename = "{}.jpg".format(str(count).zfill(16))
	cv2.imwrite(os.path.join(outputDir, filename), frame)
	
	# Display Frame And Detect Keypresses If Flag Set
	if args["display"]:
		cv2.imshow("VideoStream", frame)
		
		key = cv2.waitKey(1) & 0xFF
		
		# 'q' Pressed
		if key == ord("q"):
			break
			
	# Increment Count
	count += 1
	
	# Sleep For Specified Duration (Secs)
	time.sleep(args["delay"])
	
	
# Close Windows, Release Video Stream Pointer
print("[INFO] Cleaning Up...")
if args["display"]:
	cv2.destroyAllWindows()
vs.stop()