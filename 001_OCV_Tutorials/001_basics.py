# Import Needed Packages
import imutils
import cv2
import os


# Load Input Image From Filepath, Load And Print Dimensions
imPath = os.path.sep.join(["images", "30th_birthday.png"])
image = cv2.imread(imPath)
(h,w,d) = image.shape
print("Width={}, Height={}, Depth={}".format(w,h,d))

# Display Image Until Keypress
cv2.imshow("Image", image)
cv2.waitKey(0)


# Access BGR Values Of Px At x=430, y=200
(B,G,R) = image[200,430]
print("R={}, G={}, B={}".format(R,G,B))


# Extract 100x320 Px Square ROI
# Starting At x=150, y=80. Ending At x=250, y=400
roi = image[80:400, 150:250]
cv2.imshow("ROI", roi)
cv2.waitKey(0)


# Resize Image (Aspect Aware)
# If Using RPi:
# resized = imutils.resize(image, width=300, inter=cv2.INTER_NEAREST)
resized = imutils.resize(image, width=300)
cv2.imshow("Aspect Ratio Resize", resized)
cv2.waitKey(0)


# Rotate Image 45 Deg Clockwise
rotated = imutils.rotate(image, -45)
cv2.imshow("Rotated", rotated)
cv2.waitKey(0)


# Gaussian Blur
blurred = cv2.GaussianBlur(image, (11,11), 0)
cv2.imshow("Blurred", blurred)
cv2.waitKey(0)


# Drawing Methods
# rectangle(image, start x/y, end x/y, color, width)
cv2.rectangle(image, (150,80), (250,500), (255,0,255), 5)
# circle(image, center x/y, radius, color, thickness -- filled)
cv2.circle(image, (490,240), 30, (255,0,0), -1)
# line(image, start, end, color, thickness)
cv2.line(image, (0,0), (600,457), (0,0,255), 5)
# putText(image, text, start x/y, font, font size, color, thickness)
cv2.putText(image, "You're Learning OpenCV!", (10,45), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0),2)
cv2.imshow("Drawing", image)
cv2.waitKey(0)