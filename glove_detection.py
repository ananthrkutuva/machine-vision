import cv2
from matplotlib import pyplot as plt
import numpy as np

# Image path
path = "/home/akutuva/ros2_ws/src/machine-vision/example_handlebars.jpg"

# Input image into openCV
img = cv2.imread(path, cv2.IMREAD_COLOR)
img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Create HSV bounds for color of gloves and color of sky
red_lower = np.array([150, 145, 145])
red_upper = np.array([179, 255, 255])

red_mask = cv2.inRange(img_HSV, red_lower, red_upper)


_, binary_image = cv2.threshold(red_mask, 127, 255, cv2.THRESH_BINARY)

contours, hierarchy = 


mask_applied = cv2.bitwise_and(img, img, mask=red_mask)

# Display the original image, the mask, and the result
cv2.imshow('Original Image', img)
cv2.imshow('HSV Image', img_HSV)
cv2.imshow('Red Detected', red_mask)
cv2.imshow('Final Image', mask_applied)
cv2.waitKey(0)
cv2.destroyAllWindows()