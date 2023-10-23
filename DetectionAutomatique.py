import numpy as np
import cv2

# Load the reference image
img = cv2.imread('reference_image.png')

# Define the size of the checkerboard in terms of squares
num_cols = 8
num_rows = 5

# Find the corners of the checkerboard in the image
ret, corners = cv2.findChessboardCorners(img, (num_rows, num_cols), None)
print(ret)
# If the corners are found, draw them on the image and display it
if ret == True:
    cv2.drawChessboardCorners(img, (num_cols, num_rows), corners, ret)
    cv2.imshow('Detected Corners', img)
    cv2.waitKey()
    cv2.destroyAllWindows()

# Reshape the corner coordinates to have n rows and 2 columns
corners = corners.reshape(-1, 2)

# Print the corner coordinates
print(corners)