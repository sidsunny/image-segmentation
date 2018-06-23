from __future__ import print_function
from skimage.feature import peak_local_max
from skimage.morphology import watershed
from scipy import ndimage
import numpy as np
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "path to input image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
# apply pyramid mean shift filtering (Line 18) to help the accuracy of the thresholding step
shifted = cv2.pyrMeanShiftFiltering(image, 21, 51)
cv2.imshow("Input", image)
cv2.waitKey(0)
cv2.imshow("Mean Shifted", shifted)
cv2.waitKey(0)

gray = cv2.cvtColor(shifted, cv2.COLOR_BGR2GRAY)
# apply Otsu’s thresholding to segment the background from the foreground
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
cv2.imshow("Thresh", thresh)
cv2.waitKey(0)

# find contours in threshold image
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
print ("[INFO] {} unique contours found".format(len(cnts)))

# loop over the contours
for (i, c) in enumerate(cnts):
	# draw the contour
	((x, y), _) = cv2.minEnclosingCircle(c)
	cv2.putText(image, "#{}".format(i + 1), (int(x) - 10, int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
	cv2.drawContours(image, [c], -1, (0, 255, 0), 2)

cv2.imshow("Contours", image)
cv2.waitKey(0)

# Distance_transform_edt function computes the Euclidean distance to the closest zero (i.e., background pixel) for each of the foreground pixels
D = ndimage.distance_transform_edt(thresh)
localMax = peak_local_max(D, indices = False, min_distance = 20, labels = thresh)

# Take output of the peak_local_max function and apply a connected-component analysis using 8-connectivity. The output of this function gives markers  which is then fed into the watershed  function. Since the watershed algorithm assumes that markers represent local minima (i.e., valleys) in the distance map, negative value of D is taken
markers = ndimage.label(localMax, structure = np.ones((3, 3)))[0]

# returns a matrix of labels, one for each pixel
labels = watershed(-D, markers, mask = thresh)
print ("{} unique segments found".format(len(np.unique(labels)) - 1))


for label in np.unique(labels):

	# 0 label corresponds to background
	if label == 0:
		continue

	# allocate memory for mask  and set the pixels belonging to the current label to 255 (white)
	mask = np.zeros(gray.shape, dtype = "uint8")
	mask[labels == label] = 255

	# detect contours in the mask  and extract the largest one — this contour will represent the outline/boundary of a given object in the image
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
	c = max(cnts, key = cv2.contourArea)

	# given the contour of the object, draw the enclosing circle boundary surrounding the object
	((x, y), r) = cv2.minEnclosingCircle(c)
	cv2.circle(image, (int(x), int(y)), int(r), (0, 255, 0), 2)
	cv2.putText(image, "#{}".format(label), (int(x) - 10, int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

cv2.imshow("Output", image)
cv2.waitKey(0)