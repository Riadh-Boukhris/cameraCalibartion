import cv2
import numpy as np

pattern_size = (5, 8)  # Number of corners in the damier pattern

cap = cv2.VideoCapture('video_damier.m4v')  # Video capture from file
while cap.isOpened():
    ret, image = cap.read()
    if ret:
        # Automatic detection of corners
        retval, corners2d = cv2.findChessboardCorners(image, pattern_size)

        if retval:
            corners2d = corners2d.reshape(-1, 2)
            cv2.drawChessboardCorners(image, pattern_size, corners2d, patternWasFound=retval)

            # Calculate the center of the damier pattern
            center_x = int((corners2d[0][0] + corners2d[-1][0]) / 2)
            center_y = int((corners2d[0][1] + corners2d[-1][1]) / 2)
            # Draw a circle at the center of the damier pattern
            circle_center = (center_x, center_y)
            cv2.circle(image, circle_center, 20, (0, 0, 255), thickness=10)

            cv2.imshow('frame', image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if the job is finished
cap.release()
cv2.destroyAllWindows()
