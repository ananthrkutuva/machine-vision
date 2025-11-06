import cv2
from matplotlib import pyplot as plt
import numpy as np

# Image path
path = "/home/akutuva/ros2_ws/src/machine-vision/example_handlebars.jpg"

# Input image into openCV
original_img = cv2.imread(path, cv2.IMREAD_COLOR)
img_HSV = cv2.cvtColor(original_img, cv2.COLOR_BGR2HSV)

# Create HSV bounds for color of gloves and color of sky
red_lower = np.array([110, 145, 145])
red_upper = np.array([179, 255, 255])

red_mask = cv2.inRange(img_HSV, red_lower, red_upper)

contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

image_with_contours = cv2.drawContours(original_img, contours, -1, (0, 255, 0), 3)

# Display the original image, the mask, and the result
cv2.imshow('Original Image', original_img)
cv2.imshow('HSV Image', img_HSV)
cv2.imshow('Red Detected', red_mask)
cv2.imshow('Original Image with Contours Overlayed', image_with_contours)
# cv2.imshow('Final Image', mask_applied)
cv2.waitKey(0)
cv2.destroyAllWindows()