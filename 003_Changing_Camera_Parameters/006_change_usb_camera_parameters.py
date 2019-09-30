# More Exhaustive List Of API Flags For VideoCapture Can Be Found In The OCV Documentation:
# https://docs.opencv.org/4.1.0/d4/d15/group__videoio__flags__base.html#gaeb8dd9c89c10a5c63c139bf7c4f5704d


# Keys:
# q - Quit
# f - Auto Focus
# w - Auto White Balance
# i - Zoom In
# o - Zoom Out


# Import Needed Packages
from imutils.video import VideoStream
import time
import cv2


def toggle_autofocus(vs, autofocus=True):
	# Set AutoFocuse Camera Property
	vs.stream.set(cv2.CAP_PROP_AUTOFOCUS, 1 if autofocus else 0)
	print("[INFO] AutoFocus Set To: {}".format("ON" if autofocus else "OFF"))
	
	# Read Back Property To Ensure It Was Set
	actualAutoFocus = vs.stream.get(cv2.CAP_PROP_AUTOFOCUS)
	print("[INFO] Actual AutoFocus: {}".format(actualAutoFocus))
	
def toggle_auto_whitebalance(vs, autowb=True):
	# Set WhiteBalance Camera Property
	vs.stream.set(cv2.CAP_PROP_AUTO_WB, 1 if autowb else 0)
	print("[INFO] Auto White Balance Set To: {}".format("ON" if autowb else "OFF"))
	
	# Read Back Property To Ensure It Was Set
	actualWhiteBalance = vs.stream.get(cv2.CAP_PROP_AUTO_WB)
	print("[INFO] Actual White Balance: {}".format(actualWhiteBalance))
	
def set_zoom(vs, zoom=100):
	# Set Zoom Camera Property
	vs.stream.set(cv2.CAP_PROP_ZOOM, zoom)
	print("[INFO] Zoom Set To: {}".format(zoom))
	
	# Read Back Property To Ensure It Was Set
	actualZoom = vs.stream.get(cv2.CAP_PROP_ZOOM)
	print("[INFO] Actual Zoom: {}".format(actualZoom))
		  
		  
# Init Video Stream
vs = VideoStream(src=0).start()
time.sleep(2.0)

# Init Camera Parameter Settings
autofocus = True
autowb = True
zoom = 100


# Iterate Over Frames
while True:
	# Grab Frame
	frame = vs.read()
	
	# Display Frame
	cv2.imshow("Frame", frame)
	
	# Capture And Process Key Presses
	key = cv2.waitKey(1)
	
	# "q" Pressed: Quit
	if key == ord("q"):
		break
		
	# "f" Pressed: AutoFocus
	elif key == ord("f"):
		# Toggle AutoFocus And Set Camera Property
		autofocus = not autofocus
		toggle_autofocus(vs,autofocus)
		
	# "w" Pressed: Auto White Balance
	elif key == ord("w"):
		# Toggle Auto White Balance And Set Camera Property
		autowb = not autowb
		toggle_auto_whitebalance(vs,autowb)
		
	# "i" Pressed: Zoom In
	elif key == ord("i"):
		# Increase Zoom And Set Camera Property
		zoom += 1
		set_zoom(vs,zoom)
		
	# "o" Pressed: Zoom Out
	elif key == ord("o"):
		# Decrease Zoom And Set Camera Property
		zoom -= 1
		set_zoom(vs,zoom)
		

# Reset Camera Parameter Settings
toggle_autofocus(vs,1)
toggle_auto_whitebalance(vs,1)
set_zoom(vs,100)

# Cleanup
vs.stop()
cv2.destroyAllWindows()