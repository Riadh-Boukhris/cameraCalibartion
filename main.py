import helper 
import cv2
import numpy as np
# Distance between the camera and the checkerboard (mm)
Z = 500 

K = helper.create_K()
image = cv2.imread('reference_image.png')  # Charger l'image
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convertir l'image en niveaux de gris

# Définir la taille du damier (nombre de coins internes)
corners_x = 5
corners_y = 8
"""
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
print("Point2D + ", Point2D)

"""






#Cercle au barycentre
#REFERENCE IMAGE
cap = cv2.VideoCapture('video_damier.m4v') #0 webcam integre
pattern_size=(5,8) #Connaissance geometrie damier: nombre de cases en ligne et colonne
while(cap.isOpened()): #e.g. cam unplugged
    ret, image = cap.read()
    if ret==True:
        #Automatic detection of corners
        retval,corners2d=cv2.findChessboardCorners(image, pattern_size)
        if retval:
            corners2d=corners2d.reshape(-1,2)
            point3D = helper.pixels2camera(corners2d,K,Z)
            point3DC = helper.camera2pixels(K,point3D)
            point3DC = np.mean(point3DC, 0)            
            cv2.drawChessboardCorners(image, pattern_size, corners2d, patternWasFound=retval)
            text = "x = "+ str(point3DC[0]) 
            text1 =  "y = " + str(point3DC[1]) 
            text2 =  "z = " + str(Z)
            cv2.putText(image,text,(40,40),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255))
            cv2.putText(image,text1,(40,80),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255))
            cv2.putText(image,text2,(40,120),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255))
            frame_width = int((corners2d[0][0] + corners2d[-1][0])//2) 
            frame_height = int((corners2d[0][1] + corners2d[-1][1])//2)
            circle_center=(frame_width,frame_height)
            cv2.circle(image,circle_center, 20, (0, 0, 255), thickness=10)
            cv2.imshow('frame',image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

#Release everything if job is finished
cap.release()
#out.release()
cv2.destroyAllWindows()



#Ex4
#Définir l'arrêt du carré
size = 100
# REFERENCE IMAGE
cap = cv2.VideoCapture('video_damier.m4v')  # 0 webcam integre
pattern_size = (5, 8)  # Connaissance geometrie damier: nombre de cases en ligne et colonne
while(cap.isOpened()):  # e.g. cam unplugged
    ret, image = cap.read()
    if ret == True:
        # Automatic detection of corners
        retval, corners2d = cv2.findChessboardCorners(image, pattern_size)
        if retval:
            corners2d = corners2d.reshape(-1, 2)
            point3D = helper.pixels2camera(corners2d, K, Z)
            square = helper.create_square(corners2d, size)
            square_int = square.astype(np.int32)

            point3DC = helper.camera2pixels(K, point3D)
            point3DC = np.mean(point3DC, 0)
            cv2.drawChessboardCorners(image, pattern_size, corners2d, patternWasFound=retval)
            text = "x = " + str(point3DC[0])
            text1 = "y = " + str(point3DC[1])
            text2 = "z = " + str(Z)
            cv2.putText(image, text, (40, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
            cv2.putText(image, text1, (40, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
            cv2.putText(image, text2, (40, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
            for i in range(4):
                cv2.line(image, tuple(square_int[i]), tuple(square_int[(i+1)%4]), color=(255, 0, 0), thickness=20)
                #la fonction cv2.int attent deux points de type int_32. 
                #Pour cela, on a intéret de changer le type de notre carré (square)
                #à square_int 
                
            cv2.imshow('frame', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
# Release everything if the job is finished
cap.release()
cv2.destroyAllWindows()




