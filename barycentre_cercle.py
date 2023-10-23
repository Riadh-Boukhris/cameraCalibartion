import helper 
import cv2
import numpy as np
# Distance between the camera and the checkerboard (mm)
Z = 500 

K = helper.create_K()


# Définir la taille du damier (nombre de coins internes)
corners_x = 4
corners_y = 4


#Cercle au barycentre
#REFERENCE IMAGE
cap = cv2.VideoCapture('0') #0 webcam integre
pattern_size=(4,4) #Connaissance geometrie damier: nombre de cases en ligne et colonne
while(True): #e.g. cam unplugged
    ret, image = cap.read()
    cv2.imshow("Video", image)
    
    if ret==True & cv2.waitKey(1):
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



