# Usage:
# python 009_timelapse_process_images.py --input output/images/{dir} --output output/videos --fps 30

# Create Time Lapse Video Of Previously Captured Time Lapse Frames
# 008_capture_timelapse_frames.py


# Import Needed Packages
from imutils.video import VideoStream
from imutils import paths
import progressbar
import argparse
import cv2
import os


# Obtain Number Of Frames From Image Directory
def get_number(imagePath):
	return int(imagePath.split(os.path.sep)[-1][:-4])


# Construct Argument Parser And Parse Arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True, help="Path To Input Directory")
ap.add_argument("-o", "--output", required=True, help="Path To Output Directory")
ap.add_argument("-f", "-fps", type=int, default=30, help="FPS Of Output Video")
args = vars(ap.parse_args())


# Init FourCC And Video Writer
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
writer = None

# Grab Paths To Images, Init Output Filename And Output Path
imagePaths = list(paths.list_images(args["input"]))
outputFile = os.path.join(args["input"].split(os.path.sep)[2])
outputPath = os.path.join(args["output"], outputFile)
print("[INFO] Building {}...".format(outputPath))

# Init Progress Bar
widgets = ["Building Video: ", progressbar.Percentage(), " ", progressbar.Bar(), " ", progressbar.ETA()]
pbar = progressbar.ProgressBar(maxval=len(imagePaths), widgets=widgets).start()


# Iterate Over All Sorted Image Paths
for (i, imagePath) in enumerate(sorted(imagePaths, key=get_number)):
	# Load Image
	image = cv2.imread(imagePath)
	
	# Init Video Writer If Needed
	if writer is None:
		(H,W) = image.shape[:2]
		writer = cv2.VideoWriter(outputPath, fourcc, args["fps"], (W,H), True)
		
	# Write Image To Output Video
	writer.write(image)
	pbar.update(i)
	
	
# Release Write Object
print("[INFO] Cleaning Up...")
pbar.finish()
writer.release()