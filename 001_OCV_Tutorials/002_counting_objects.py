# Usage:
# python 002_counting_objects.py --image  images/shapes.png


# Import Needed Packages
import argparse
import imutils
import cv2


# Construct Argument Parser And Parse Arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path To Image")
args = vars(ap.parse_args())


# Load Image, Convert to Grayscale, Blur, Canny
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (3,3), 0)
edged = cv2.Canny(blurred, 50, 130)


# Find Contours In Edge Map, Init Total Number Of Shapes Found
# findContours Processes Edged Image And Accumulates A List Of (X,y)-Coords
# For Each, Separate Outline. Since The Return Signature Is Different Between
# OpenCV Versions, We Use imutils.grab_contours Method To Parse The Returned
# Tuple And Return Out List Of Contours
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
total = 0

# Iterate Over Contours
for c in cnts:
	# If Contour Area Is Small, Ignore (Most Likely Noise)
	if cv2.contourArea(c) < 25:
		continue
	
	# Otherwise, Draw Contour On Image And Increment Total Found
	cv2.drawContours(image, [c], -1, (204,0,255), 2)
	total += 1
	
# Show Output Image And Final Shape Count
print("[INFO] Found {} Shapes".format(total))
cv2.imshow("Image", image)
cv2.waitKey(0)