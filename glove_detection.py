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

x_coords = []
y_coords = []

for contour in contours:
    reshaped_contour = contour.reshape(-1, 2)
    contour_x_vals = reshaped_contour[:, 0]
    contour_y_vals = reshaped_contour[:, 1]
    x_coords.append(contour_x_vals)
    y_coords.append(contour_y_vals)

x_arr = np.array(x_coords, dtype=object)
y_arr = np.array(y_coords, dtype=object)

min_x_vals = np.empty(0)

for x_val_arr in x_arr:
    min_x_vals = np.append(min_x_vals, x_val_arr[0])

print(min_x_vals)

middle_threshold_val = min_x_vals > 300

idx_threshold = np.argmax(middle_threshold_val)

# print("X Array")
# print(x_arr)

# middle_threshold = 300

# left_glove_x_vals = 


# print("First X Coordinates")
# print(x_coords[0])
# print("All X coordinates")
# print(x_coords)
# print("First Y Coordinates")
# print(y_coords[0])
# print("All Y coordinates")
# print(y_coords)

# print("All Contours")
# print(contours)



image_with_contours = cv2.drawContours(original_img, contours, -1, (0, 255, 0), 3)

# Display the original image, the mask, and the result
cv2.imshow('Original Image', original_img)
cv2.imshow('HSV Image', img_HSV)
cv2.imshow('Red Detected', red_mask)
cv2.imshow('Original Image with Contours Overlayed', image_with_contours)
# cv2.imshow('Final Image', mask_applied)
cv2.waitKey(0)
cv2.destroyAllWindows()