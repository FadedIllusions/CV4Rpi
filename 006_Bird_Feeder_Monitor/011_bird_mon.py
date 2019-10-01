# Usage:
# python 011_bird_mon.py --conf config/mog.json --video birds_10min.mp4


# In Order To Successfully Apply Background Subtraction, We Need To Make The Assumption That Our
# Background Is Mostly Static And Unchanging Over Consecutive Frames Of A Video

# Note That This Approach Has Many Limitations; Though, Is Being Used As A "Feet Wet" Exercise

# When Saving Motion Videos, How Can We Ensure That You Capture That Very Split Second Where The
# Motion Starts? By Buffering Frames. Keep The Camera Rolling At All Times And Buffer Frames So 
# That There Is Padding On The Front And Back Of A Motion Event.

# Project Implements Key Event Writing From 2016 PyImageSearch Tutorial Titled "Saving Key Event
# Video Clips With OpenCV" (http://pyimg.co/hvskf). . . The Algorithm Maintains A Buffer Of Frames
# And, Then, Dumps Frames To Disk If Motion Is Detected, Ensuring You Have The Frames That, Not Only,
# Include The Motion; But, Also, Frames Leading Up To The Motion.


# Import Needed Packages
from helpers.keyclipwriter import KeyClipWriter
from imutils.video import VideoStream
from helpers.utils import Conf
import numpy as np
import argparse
import datetime
import imutils
import signal
import time
import sys
import cv2
import os


# External Interrupt Handler ('ctrl+c')
def signal_handler(sig, frame):
	# Display Message To User
	print("\n[INFO] 'ctrl+c' Pressed...")
	print("\n[INFO] Files Saved In '{}' Directory".format(conf["output_path"]))
	
	# Wrap-Up If Recording
	if kcw.recording:
		kcw.finish()
		
	sys.exit(0)
	
	
# Construct Argument Parser And Parse Arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--conf", required=True, help="Path To JSON Config File")
ap.add_argument("-v", "--video", type=str, help="Path To (Optional) Input Video File")
args = vars(ap.parse_args())


# Load Configuration Settings
conf = Conf(args["conf"])


# If Using Camera, Start Stream
if not args.get("video", False):
	print("[INFO] Starting Video Stream...")
	vs = VideoStream(usePiCamera=conf["picamera"]).start()
	time.sleep(3.0)
	
else:
	print("[INFO] Opening Video File '{}'".format(args["video"]))
	vs = cv2.VideoCapture(args["video"])
	
	
# OpenCV Background Subtractors
OPENCV_BG_SUBTRACTORS = {
	"CNT": cv2.bgsegm.createBackgroundSubtractorCNT,
	"GMG": cv2.bgsegm.createBackgroundSubtractorGMG,
	"MOG": cv2.bgsegm.createBackgroundSubtractorMOG,
	"GSOC": cv2.bgsegm.createBackgroundSubtractorGSOC,
	"LSBP": cv2.bgsegm.createBackgroundSubtractorLSBP
}

# Create Background Subtractor
fgbg = OPENCV_BG_SUBTRACTORS[conf["bg_sub"]]()


# Create Erosion And Dilation Kernels
eKernel = np.ones(tuple(conf["erode"]["kernel"]), "uint8")
dKernel = np.ones(tuple(conf["dilate"]["kernel"]), "uint8")


# Init Key Clip Writer, The Consecutive Number Of Frames Without Motion,
# And Frames Since Last Snapshot Was Written
kcw = KeyClipWriter(bufSize=conf["keyclipwriter_buffersize"])
framesWithoutMotion = 0
framesSinceSnap = 0


# Begin Capturing Interrupt Signals
signal.signal(signal.SIGINT, signal_handler)
images = " And Images..." if conf["write_snaps"] else "..."
print("[INFO] Detecting Motion And Storing Videos{}".format(images))


# Iterate Over Frames
while True:
	# Grab Frame
	fullFrame = vs.read()
	
	# If No Frame, Stream Ended
	if fullFrame is None:
		break
		
	# Handle Fram Whether Frame Was Read From VideoCapture Or VideoStream
	fullFrame = fullFrame[1] if args.get("video", False) else FullFrame
	
	# Increment Frames Since Snapshot
	framesSinceSnap += 1
	
	# Resize Fram, Apply BG Subtractor To Generate Motion Mask
	frame = imutils.resize(fullFrame, width=500)
	mask = fgbg.apply(frame)
	
	# Perform Erotions/Dilations To Eliminate Noise And Fill Gaps
	mask = cv2.erode(mask, eKernel, iterations=conf["erode"]["iterations"])
	mask = cv2.dilate(mask, dKernel, iterations=conf["dilate"]["iterations"])
	
	# Find Contours In Mask And Reset Motion Status
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	motionThisFrame = False
	
	# Iterate Over Contours
	for c in cnts:
		# Compute Bounding Circle And Rectangle For Contour
		((x,y), radius) = cv2.minEnclosingCircle(c)
		(rx,ry,rw,rh) = cv2.boundingRect(c)
		
		# Convert Floating Point Values To Ints
		(x,y,radius) = [int(v) for v in (x,y,radius)]
		
		# Only Process Motion Contours Above Specified Size
		if radius<conf["min_radius"]:
			continue
			
		# Grab Current Timestamp
		timestamp = datetime.datetime.now()
		timestring = timestamp.strftime("%Y%m%d-%H%M%S")
		
		# Set Motion Flag To Indicate Motion
		# Reset Motion Counter
		motionThisFrame = True
		framesWithoutMotion = 0
		
		# Check If Need To Annotate Frame For Display
		if conf["annotate"]:
			cv2.circle(frame, (x,y), radius, (0,0,255), 2)
			cv2.rectangle(frame, (rx,ry), (rx+rw,ry+rh), (0,255,0), 2)
			
		# Frame To Disk
		writeFrame = framesSinceSnap >= conf["frames_between_snaps"]
		
		# Check If Should Write Frame To Disk
		if conf["write_snaps"] and writeFrame:
			# Construct Path To Output Photo And Save
			snapPath = os.path.sep.join([conf["output_path"], timestring])
			cv2.imwrite(snapPath+".jpg", fullFrame)
			
			# Reset Counter Between Snapshots
			framesSinceSnap = 0
			
		# Start Recording, If Not Already
		if not kcw.recording:
			# Construct Path To Video File
			videoPath = os.path.sep.join([conf["output_path"], timestring])
			
			# Instantiate Codec Object And Start KCW
			fourcc = cv2.VideoWriter_fourcc(*conf["codec"])
			kcw.start("{}.avi".format(videoPath), fourcc, conf["fps"])
			
	# Check In No Motion Was Detected In Frame, Increment Number Of Frames Without Motion
	if not motionThisFrame:
		framesWithoutMotion += 1
		
	# Update Key Frame Clip Buffer
	kcw.update(frame)
	
	# Check If Number Of Frames Without Motion Is Above Threshold
	noMotion = framesWithoutMotion >= conf["keyclipwriter_buffersize"]
	
	# Stop Recording If No Motion
	if kcw.recording and noMotion:
		kcw.finish()
		
	# Check If Displaying Frames To Screen
	if conf["display"]:
		# Display Frame
		cv2.imshow("Video Stream", frame)
		
		# Grab Keypresses
		key = cv2.waitKey(1) & 0xFF
		
		# 'q' Pressed: Quit
		if key == ord("q"):
			break
			
			
# Cleanup
if kcw.recording:
	kcw.finish()

vs.stop if not args.get("video", False) else vs.release()