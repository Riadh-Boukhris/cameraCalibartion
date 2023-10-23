import numpy as np


# Define the 3D object points
object_points = np.array([
    [0, 0, 0],     # Object point 1
    [1, 0, 0],     # Object point 2
    [0, 1, 0]    # Object point 3
    
], dtype=np.float32)

# Define the corresponding 2D image points
image_points = np.array([
    [100, 200],    # Image point 1
    [150, 250],    # Image point 2
    [200, 180]    # Image point 3
    
], dtype=np.float32)


def create_K(dx, dy, Z, image_size, dX, dY):
    # Calculate the focal length along x and y axes
    fx = (dx * Z) / dX
    fy = (dy * Z) / dY

    # Calculate the principal point (assumed to be at the center of the image)
    cx = image_size[1] / 2
    cy = image_size[0] / 2

    # Create the intrinsic matrix K
    K = np.zeros((3, 3))
    K[0, 0] = fx
    K[1, 1] = fy
    K[0, 2] = cx
    K[1, 2] = cy
    K[2, 2] = 1

    return K

import cv2


image_size = (480, 640)




# Capture and process calibration images to populate object_points and image_points

# Run camera calibration
ret, camera_matrix, distortion_coeffs, rvecs, tvecs = cv2.calibrateCamera(
    object_points, image_points, image_size, None, None
)

# Print the camera matrix and distortion coefficients
print("Calibrated camera matrix:")
print(camera_matrix)

print("Calibrated distortion coefficients:")
print(distortion_coeffs)
