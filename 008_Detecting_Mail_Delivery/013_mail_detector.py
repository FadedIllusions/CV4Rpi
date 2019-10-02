# USAGE
# python 013_mail_detector.py --conf config/config.json


# Import Needed Packages
from helpers.notifications import TwilioNotifier
from helpers.utils import Conf
from imutils.video import VideoStream
from datetime import datetime
from datetime import date
import numpy as np
import argparse
import imutils
import signal
import time
import cv2
import sys


# Keyboard Interrupt Handler
def signal_handler(sig, frame):
	# Stop Stream And Exit
	print("[INFO] 'ctrl+c' Pressed: Closing Mail Detector Application.")
	vs.stop()
	sys.exit(o)
	
	
# Construct Argument Parser And Parse Arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--conf", required=True, help="Path To Input Configuration File")
args = vars(ap.parse_args())


# Load Config Gile And Init Twilio Notifier
conf = Conf(args["conf"])
tn = TwilioNotifier(conf)

# Init Flags -- Mailbox Open, Notification Sent
mailboxOpen = False
notifSent = False


# Init Video Stream
print("[INFO] Warming Camera Sensor, Starting Camera...")
vs = VideoStream(src=0).start()
#vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)

# Signal Trap To Handle Keyboard Interrupt
signal.signal(signal.SIGINT, signal_handler)
print("[INFO] Press 'ctrl+c' To Quit...")


# Iterate Over Frames
while True:
	# Grab Frame, Resize, Convert To Grayscale
	frame = vs.read()
	frame = imutils.resize(frame, width=200)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	
	# Set Previous Mailbox Status
	mailboxPrevOpen = mailboxOpen
	
	# Calculate Average Of All PXs Where A Higher Mean Indicates There Is
	# More Light Coming In; Then, Determine If Mailbox Open
	mean = np.mean(gray)
	mailboxOpen = mean > conf["thresh"]
	
	# If Mailbox Open And Previously Closed, Mailbox Just Opened
	if mailboxOpen and not mailboxPrevOpen:
		# Record Start Time
		startTime = datetime.now()
		
	# If Mailbox Open, There Are 2 Possibilities:
	# 1) Left Open For More Than Threshold Seconds
	# 2) Closed In Less Than Or Equal To Threshold Seconds
	elif mailboxPrevOpen:
		# Determine If Left Open Longer Than Threshold
		elapsedTime = (datetime.now()-startTime).seconds
		mailboxLeftOpen = elapsedTime > conf["open_threshold_seconds"]
			
		# Handle When Mailbox Left Open
		if mailboxOpen and mailboxLeftOpen:
			# If Notification Not Sent, Send
			if not notifSent:
				# Build Message And Send
				msg = "Your Mailbox At {} Has Been Left Open For Longer Than {} " \
				" Seconds. It Is Possible That You Or The Mailman Didn't Close " \
				"The Mailbox.".format(conf["address_id"], conf["open_threshold_seconds"])
				tn.send(msg)
				notifSent = True
		
		# Check If Mailbox Has Been Closed
		elif not mailboxOpen:
			# If Notification Already Sent, Reset
			if notifSent:
				notifSent = False
				
			# If Notification /Not/ Sent, Send Notification
			else:
				# Record End Time And Calculate Total Time
				endTime = datetime.now()
				totalSeconds = (endTime - startTime).seconds
				dateOpened = date.today().strftime("%A, %B %d %Y")
			
				# Build Message And Send
				msg = "Your Mailbox At {} Was Opened On {} At {} For {} Seconds.". format(
					conf["address_id"], dateOpened, startTime.strftime("%I:%M%p"), totalSeconds)
				tn.send(msg)
			
	# Check If Display Frame To Screen
	if conf["display"]:
		# Display Frame
		cv2.imshow("Video Stream", frame)
		
		# Record Keypress
		key = cv2.waitKey(1) & 0xff
		if key == ord("q"):
			break
			
			
# Stop Video Stream And Cleanup
cv2.destroyAllWindows()
vs.stop()