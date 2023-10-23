import numpy as np
import helper 
import cv2

import time

# Distance between the camera and the checkerboard (mm)
Z = 500


# Image size
image_width = 960
image_height = 540

# Number of corners in the checkerboard
corners_x = 5
corners_y = 8



# Checkerboard size in real-world coordinates (mm)
checkerboard_width = 155
checkerboard_height = 105


# Calculate the pixel size of each checkerboard square
pixel_width = image_width / corners_x
pixel_height = image_height / corners_y

# Calculate the focal lengths (in pixels)
focal_length_x = (Z * pixel_width) / checkerboard_width
focal_length_y = (Z * pixel_height) / checkerboard_height

# Calculate the optical center (assuming it is at the image center)
optical_center_x = image_width / 2
optical_center_y = image_height / 2

K = helper.create_K()
print("Matrice intrinséque K = ",K)

#image = cv2.imread('reference_image.png')  # Charger l'image
pose = cv2.imread('ex3_pose_3.png')
gray = cv2.cvtColor(pose, cv2.COLOR_BGR2GRAY)  # Convertir l'image en niveaux de gris

# Définir la taille du damier (nombre de coins internes)
corners_x = 5
corners_y = 8

# Trouver les coins du damier dans l'image


# Load the reference image
image_reference = cv2.imread('reference_image.png')
pattern_size = (5, 8)
# Trouver les coins du damier dans l'image
ret, corners = cv2.findChessboardCorners(gray, (corners_x, corners_y), None)

if ret:
    # Reformater les coordonnées des coins
    corners = corners.reshape(-1, 2)
   
    # Dessiner les coins sur l'image
    cv2.drawChessboardCorners(pose, (corners_x, corners_y), corners, ret)
    
    # Afficher l'image avec les coins détectés
    cv2.imshow('Chessboard Corners', pose)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Les coins du damier n'ont pas été trouvés dans l'image.")

# Calculate the 3D coordinates of chessboard corners in the reference image

point3D = helper.pixels2camera(corners,K,Z)
print("Point3D", point3D)


point2DW = helper.camera2pixels(point3D, K)


# Load the reference image
image_reference = cv2.imread('reference_image.png')
retval, corners_ref = cv2.findChessboardCorners(image_reference, pattern_size)
corners_3d_ref = helper.pixels2camera(corners_ref, K, Z)

# Load the current image
image_current = cv2.imread('pose2.png')



# Compute the extrinsic matrix
M_ext = helper.compute_extrinsic_matrix(point3D, point2DW, K, True)

# Compute the projection matrix
P = np.dot(K, M_ext)
print("P is here", P)
# Perform further processing with the projection matrix P
# ...
