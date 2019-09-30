# Usage:
# python 003_image_sub.py --bg images/bg.jpg --fg images/adrian.jpg


# Import Needed Packages
import numpy as np
import argparse
import imutils
import cv2


# Construct Argument Parser And Parse Arguments
ap = argparse.ArgumentParser()
ap.add_argument("-b", "--bg", required=True, help="Path To Background Image")
ap.add_argument("-f", "--fg", required=True, help="Path To Foreground Image")
args = vars(ap.parse_args())


# Load Background And Foreground Images
bg = cv2.imread(args["bg"])
fg = cv2.imread(args["fg"])

# Convert Images To Grayscale
bgGray = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY)
fgGray = cv2.cvtColor(fg, cv2.COLOR_BGR2GRAY)


# Perform Background Subtraction By Subtracting The Foreground From
# The Background And Taking Absolute Value
# By Default, OpenCV Represents Images As 8-Bit UInts; So, We
# Convert Images To 32-Bit Ints To Ensure We Can Have Negative Values
sub = bgGray.astype("int32") - fgGray.astype("int32")
sub = np.absolute(sub).astype("uint8")


# Now We Must Use Contour Detection In Order To Actually Detect
# And Extract Regions Of Image Containing Difference
# Contour Detection Assumes We Are Working With A Binary Image;
# So, We Must Binarize Image

# Threshold Image (To Binarize)
# Background Values Now 0 And Foreground 255
thresh = cv2.threshold(sub, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

# Perform Erosion And Dialations To Remove Noise
thresh = cv2.erode(thresh, None, iterations=1)
thresh = cv2.dilate(thresh, None, iterations=1)


# Apply Contour Detection To Extract Individual Regions
# Define Four Vars Which Will Be Used To Compute Bounding Box
# Encompassin ALL Foreground Regions, Thereby Giving Us A Rectangular
# Region That Contains All Significant Differences
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
(minX,minY) = (np.inf, np.inf)
(maxX,maxY) = (-np.inf, -np.inf)

# Iterate Over Contours
for c in cnts:
	# Compute Bounding Box Of Contour
	(x,y,w,h) = cv2.boundingRect(c)
	
	# Reduce Noise
	if w>20 and h>20:
		# Update Vars
		minX = min(minX, x)
		minY = min(minY, y)
		maxX = max(maxX, x+w-1)
		maxY = max(maxY, y+h-1)

		
# Draw Rectangle Surrounding Region Of Motion
cv2.rectangle(fg, (minX,minY), (maxX, maxY), (0,255,0), 2)


# Display Image
cv2.imshow("Output", fg)
cv2.waitKey(0)