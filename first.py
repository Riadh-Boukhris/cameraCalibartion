import cv2
import helper
import numpy as np

cap = cv2.VideoCapture(0)






"""

objp = np.zeros((4*4, 3), np.float32)
objp[:,:2] = np.mgrid[0:4, 0:4].T.reshape(-1,2)
objp = np.array([[ 0.,  0.,  0.],
   [ 1.,  0.,  0.],
   [ 2.,  0.,  0.],
   [ 3.,  0.,  0.],
   [ 0.,  1.,  0.],
   [ 1.,  1.,  0.],
   [ 2.,  1.,  0.],
   [ 3.,  1.,  0.],
   [ 0.,  2.,  0.],
   [ 1.,  2.,  0.],
   [ 2.,  2.,  0.],
   [ 3.,  2.,  0.],
   [ 0.,  3.,  0.],
   [ 1.,  3.,  0.],
   [ 2.,  3.,  0.],
   [ 3.,  3.,  0.]], dtype=np.float32)



"""















pattern_size = (4, 4)
while True:
    success,image = cap.read()
    imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    cv2.imshow("frame", imageGray)
    widh, height = 480, 640
    pts1 = np.float32([[0, 0], [0, widh ], [0, height], [widh, height]])

    if success == True:
        
        #Automatic detection of corners
        retval, corners2d=cv2.findChessboardCorners(imageGray, pattern_size)
        
        if retval:
            corners2d=corners2d.reshape(-1,2)           
            cv2.drawChessboardCorners(imageGray, pattern_size, corners2d, patternWasFound=retval)
            frame_width = int((corners2d[0][0] + corners2d[-1][0])//2) 
            frame_height = int((corners2d[0][1] + corners2d[-1][1])//2)
            circle_center=(frame_width,frame_height)
            cv2.circle(imageGray,circle_center, 20, (0, 0, 255), thickness=10)
            cv2.imshow('frame',imageGray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
print(image.shape)
cap.release()
cv2.destroyAllWindows()

"""
imageGray = cv2.resize(image, (1200,640))
cv2.imshow("Image", imageGray)
cv2.waitKey(0)
"""
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objp, corners2d, objp[::-1],None,None)

print(mtx, dist)