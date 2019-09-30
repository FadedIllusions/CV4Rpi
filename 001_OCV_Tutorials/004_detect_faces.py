# Usage:
# python 004_detect_faces.py --image images/faces_example.png


# Import Needed Packages
import argparse
import cv2


# Construct Argument Parser And Parse Arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path To Input Image")
args = vars(ap.parse_args())


# Load Image, Convert To Grayscale
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Load Detector And Detect Faces In Image
haar = "haarcascade_frontalface_default.xml"
detector = cv2.CascadeClassifier(haar)
rects = detector.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=9, 
								  minSize=(40,40), flags=cv2.CASCADE_SCALE_IMAGE)
print("[INFO] Detected {} Faces".format(len(rects)))

# Iterate Over Bounding Boxes And Draw Rectangle Around Each Face
for (x,y,w,h) in rects:
	cv2.rectangle(image, (x,y), (x+w,y+h), (0,255,0), 2)
	
# Display Detected Faces
cv2.imshow("Faces", image)
cv2.waitKey(0)