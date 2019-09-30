# Press 'q' To Escape Video Streaming

# Import Needed Packages
from imutils.video import VideoStream
import imutils
import time
import cv2


# Init Video Stream And Allow Camera Sensor Time To Warmup
print("[INFO] Starting Video Stream...")
vs = VideoStream(src=0).start()
# vs = VideoStream(usePiCamera=True, resolution=(640,480)).start()
time.sleep(2.0)


# Iterate Over Frames
while True:
	# Grab Frame, Resize To Max Width 400
	frame = vs.read()
	frame = imutils.resize(frame, width=400)
	
	# Display Output Frame
	cv2.imshow("Frame", frame)
	
	# Construct Escape Sequence
	key = cv2.waitKey(1) & 0xFF
	
	if key == ord("q"):
		break
		
# Cleanup
cv2.destroyAllWindows()
vs.stop()