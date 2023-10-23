import helper 
import cv2
import numpy as np
# Distance between the camera and the checkerboard (mm)
Z = 500 

K = helper.create_K()
print("K = ", K)
image = cv2.imread('reference_image.png')  # Charger l'image
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convertir l'image en niveaux de gris

# Définir la taille du damier (nombre de coins internes)
corners_x = 5
corners_y = 8

# Trouver les coins du damier dans l'image
ret, corners = cv2.findChessboardCorners(gray, (corners_x, corners_y), None)

if ret:
    # Reformater les coordonnées des coins
    corners = corners.reshape(-1, 2)
   
    # Dessiner les coins sur l'image
    cv2.drawChessboardCorners(image, (corners_x, corners_y), corners, ret)
    
    # Afficher l'image avec les coins détectés
    cv2.imshow('Chessboard Corners', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Les coins du damier n'ont pas été trouvés dans l'image.")
point3D = helper.pixels2camera(corners,K,Z)
print("Point3D = ", point3D)

Point2D = helper.camera2pixels(point3D, K)
print("Point2D = ", Point2D)
