import cv2
from matplotlib import pyplot as plt
import numpy as np

# Image path
path = "/home/akutuva/ros2_ws/src/machine-vision/example_handlebars.jpg"

# Input image into openCV
img = cv2.imread(path, cv2.IMREAD_COLOR)
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Show the image
cv2.imshow('Original Image', img)
cv2.imshow('RGB Image', img_rgb)

# Wait until any key is pressed
cv2.waitKey(0)

# Once a key is pressed, close the window
cv2.destroyAllWindows()