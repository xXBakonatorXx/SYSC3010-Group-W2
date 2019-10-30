import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar



if __name__ == "__main__":
    #img = cv2.imread("line0.png")
    cap = cv2.VideoCapture(0)
    threshold = 200
    while (True):
        _, img = cap.read()
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
        print(img[0][0])

        
        height, width = img.shape[0:2]
        print(height, width)
        for y in range(height-1):
            for x in range(width-1):
                if abs(img[y+1][x] - img[y][x]) > threshold:
                    img[y][x] = 255
                else:
                    img[y][x] = 0

                if abs(img[y][x+1] - img[y][x]) > threshold:
                    img[y][x] = 255
                else:
                    img[y][x] = 0


        cv2.imshow("img", img)
        key = cv2.waitKey(1)
        if key == 27:
            break
    #cv2.waitKey(0)