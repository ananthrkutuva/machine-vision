import cv2
from matplotlib import pyplot as plt
import numpy as np

# Image path
path = "/home/akutuva/ros2_ws/src/machine-vision/example_handlebars.jpg"

# Input image into openCV
img = cv2.imread(path, cv2.IMREAD_COLOR)
img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Create HSV bounds for color of gloves and color of sky
red_lower = np.array([0, 145, 145])
red_upper = np.array([179, 255, 255])

blue_lower = np.array([223, 40, 70])
blue_upper = np.array([225, 255, 255])

result = cv2.inRange(img_HSV, red_lower, red_upper)

# Display the original image, the mask, and the result
cv2.imshow('Original Image', img)
cv2.imshow('HSV Image', img_HSV)
# cv2.imshow('Red Mask', red_mask)
cv2.imshow('Red Detected', result)
cv2.waitKey(0)
cv2.destroyAllWindows()