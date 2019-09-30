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
from itertools import cycle
from pprint import pprint
import time
import cv2


# Set Video Stream As Global Variable
global vs


def get_picam_settings(output=False):
	# Access Globals
	global picamSettings
	global vs
	
	# Init Variable To Hold Current Settings
	currentPicamSettings={}
	
	# Init Status Message If Output Will Be Displayed
	if output:
		print("[INFO] Reading Settings...")
		
	# Grab PiCamera Attributes From Object
	for attr in picamSettings.keys():
		currentPicamSettings[attr] = getattr(vs.camera,attr)
		
		# Print Settings To Terminal, If Required
		if output:
			pprint(currentPicamSettings)
			
		# Update The Global
		picamSettings = currentPicamSettings
		
		# Return Settings To Calling Function
		return currentPicamSettings
	
def get_single_picam_settings(setting):
	currentPicamSettings = get_picam_settings()
	return currentPicamSettings[setting]

def _set_picam_settings(**kwargs):
	# Create New Video Stream With Settings
	global vs
	vs.stop()
	time.sleep(0.25)
	vs = VideoStream(usePiCamera=True, **kwargs).start()
	time.sleep(1.5)
	
	print("[INFO] Success...")
	
def set_picam_setting(**kwargs):
	# Access Globals
	global picamSettings
	global vs
	
	# Read Current Settings
	print("[INFO] Reading Settings...")
	currentPicamSettings = get_picam_settings()
	
	# Print Past And New Values
	for (attr, value) in kwargs.items():
		print("[INFO] Changing {} From {} To {}".format(attr, currentPicamSettings[attr],value))
		currentPicamSettings[attr] = value
		
	# Init Var To Hold Duplicate Attributes To Delete
	# Since We Can't Have Duplicates In kwargs
	attrsToDel=[]
	
	# Iterate Over Current Setting Attributes
	for attr in currentPicamSettings.keys():
		# Test For Value of None
		if currentPicamSettings[attr] == None:
			attrsToDel.append(attr)
	
	# Delete All Duplicate Attributes
	for attr in attrsToDel:
		currentPicamSettings.pop(attr)
		_set_picam_setting(**kwargs)
		
		
# Init Video Steam
vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)


# Auto White Balance And ISO Modes
awbModes = ["off", "auto", "sunlight", "cloudy", "shade", "tungsten", "flourescent", "flash", "horizon"]
isoModes = [0, 100, 200, 320, 400, 500, 640, 800, 1600]

# Init Two Cycle Pools
isoModesPool = cycle(isoModes)
awbModesPool = cycle(awbModes)

# The Following Dictionary Consists of PiCamera Attribute That Can Be 'Changed';
# The List Is Not Exhaustive Because Some Settings Can Only Be Changed Based on
# Values Of Others. Be Sure To Refer To Docs
picamSettings = {
	"awb_mode": None,
	"awb_gains": None,
	"brightness": None,
	"color_effects": None,
	"contrast": None,
	"drc_strength": None,
	"exposure_compensation": None,
	"exposure_mode": None,
	"flash_mode": None,
	"hflip": None,
	"image_denoise": None,
	"image_effect": None,
	"image_effect_params": None,
	"iso": None,
	"meter_mode": None,
	"rotation": None,
	"saturation": None,
	"sensor_mode": None,
	"sharpness": None,
	"shutter_speed": None,
	"vflip": None,
	"video_denoise": None,
	"video_stabilization": None,
	"zoom": None
}


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
		
	# "w" Pressed: Auto White Balance
	elif key == ord("w"):
		# Read White Balance Mode And Change It
		awbMode = get_single_picam_setting("awb_mode")
		set_picam_setting(awb_mode=next(awbModesPool))
		
	# "i" Pressed: ISO
	elif key == ord("i"):
		# Read ISO And Increase (Looping After 1600)
		iso = get_single_picam_setting("iso")
		set_picam_setting(iso=next(isoModesPool))
		
	# "b" Pressed: Brightness
	elif key == ord("b"):
		# Read Brightness And Increase
		brightness = get_single_picam_setting("brightness")
		brightness += 1
		set_picam_setting(brightness=brightness)
		
	# "d" Pressed: Darken Brightness
	elif key == ord("d"):
		# Read Brightness And Decrease
		brightness = get_simgle_picam_setting("brightness")
		brightness -= 1
		set_picam_setting(brightness=brightness)
		
	# "r" Pressed: Read Settings
	elif key == ord("r"):
		get_picam_settings(output=True)
		
	# "c" Pressed: Custom Settings
	elif key == ord("c"):
		set_picam_setting(brightness=30, iso=800, awb_mode="cloudy", vflip=True)
		

# Cleanup
vs.stop()
cv2.destroyAllWindows()


	

