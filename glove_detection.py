import cv2
from matplotlib import pyplot as plt
import numpy as np
import math

# Image path
path = "/home/akutuva/ros2_ws/src/machine-vision/data/example_handlebars.jpg"

# Input image into openCV
original_img = cv2.imread(path, cv2.IMREAD_COLOR)
img_HSV = cv2.cvtColor(original_img, cv2.COLOR_BGR2HSV)

# Create HSV bounds for color of gloves
red_lower = np.array([110, 145, 145])
red_upper = np.array([179, 255, 255])

# Create a mask that will filter out all pixels outside the given HSV range. The pixels within the range will be white, all others will be black, a binary image.
red_mask = cv2.inRange(img_HSV, red_lower, red_upper)

# Generate contours around all white pixels in the image
contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Make lists to hold many arrays of the x and y coordinates of the contour pixels. Each array in the list contains the respective x coordinates of each contour
x_coords = []
y_coords = []

# For each contour in the overall contours list, extract the x and y coordinates into their own lists
for contour in contours:
    reshaped_contour = contour.reshape(-1, 2)
    contour_x_vals = reshaped_contour[:, 0]
    contour_y_vals = reshaped_contour[:, 1]
    x_coords.append(contour_x_vals)
    y_coords.append(contour_y_vals)

# print(x_coords)

# Make arrays for all the x and y coordinates
x_arr = np.array(x_coords, dtype=object)
y_arr = np.array(y_coords, dtype=object)

# Starting with processing the x values first
min_x_vals = np.empty(0)

# For every array of x coordinates in the x value array, extract the minimum value and put this into its own array
for x_val_arr in x_arr:
    min_x_vals = np.append(min_x_vals, x_val_arr[0])

# print(min_x_vals)

middle_pixel_val = 300

# Using the array of minimum x values in each array of x values, make a boolean array recording if each array in the list is greater than the middle value
min_boolean_array = min_x_vals > middle_pixel_val

# Find the first array in the list that is True, meaning that all entries before this are part of the left part of the image
idx_threshold = np.argmax(min_boolean_array)

# Make an array to hold the left x contours
left_glove_x_arrs = np.empty(0)

# Combine all arrays from the x contours to get one list of all x coordinates that make up the left glove contour
left_glove_x_arrs = np.concatenate(x_arr[0:idx_threshold])

# print(left_glove_arrs)

# Calculate the mean x value of the left glove
avg_left_x_coord = np.round(np.mean(left_glove_x_arrs))

# Using the remaining arrays in the x contours for the right glove
right_glove_x_arrs = np.concatenate(x_arr[idx_threshold:])
avg_right_x_coord = np.round(np.mean(right_glove_x_arrs))

# Doing the same process for the y coordinates for the left and right gloves
left_glove_y_arrs = np.empty(0)
left_glove_y_arrs = np.concatenate(y_arr[0:idx_threshold])
avg_left_y_coord = np.round(np.mean(left_glove_y_arrs))

right_glove_y_arrs = np.empty(0)
right_glove_y_arrs = np.concatenate(y_arr[idx_threshold:])
avg_right_y_coord = np.round(np.mean(right_glove_y_arrs))

# print("Average Left X: " + str(avg_left_x_coord))
# print("Average Left Y: " + str(avg_left_y_coord))
# print("Average Right X: " + str(avg_right_x_coord))
# print("Average Right Y: " + str(avg_right_y_coord))

image_with_contours = cv2.drawContours(original_img, contours, -1, (0, 255, 0), 3)

# Visualization
# Drawing the calculated center of mass points on the image
start_point = (int(avg_left_x_coord), int(avg_left_y_coord))
end_point = (int(avg_right_x_coord), int(avg_right_y_coord))

points = [start_point, end_point]
for point in points:
    cv2.circle(image_with_contours, point, 6, (255, 0 , 0), -5)

cv2.line(image_with_contours, start_point, end_point, (0, 255, 255), 5)

# Calculating the angle of the line
delta_x = avg_left_x_coord - avg_right_x_coord
delta_y = avg_left_y_coord - avg_right_y_coord

angle = round(math.atan2(delta_y, delta_x), 3)

print("Angle: " + str(angle) + " Degrees")

# Display the original image, the mask, and the result
cv2.imshow('Original Image', original_img)
cv2.imshow('HSV Image', img_HSV)
cv2.imshow('Red Detected', red_mask)
cv2.imshow('Original Image with Contours Overlayed', image_with_contours)
# cv2.imshow('Final Image', mask_applied)
cv2.waitKey(0)
cv2.destroyAllWindows()