import os
import sys
import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar

class Capture:
    def __init__(self, adapter=0, line_threshold=150, edge_threshold1=200, edge_threshold2=255, tolerance=0.9):
        self.__adpater__        = adapter
        self.__capture__        = None
        self.__lineThreshold__  = line_threshold
        self.__edgeThreshold1__ = edge_threshold1
        self.__edgeThreshold2__ = edge_threshold2

        #flags
        self.QR      = 0x1
        self.LINE    = 0x2
        self.DISPLAY = 0x4
        self.EDGE    = 0x8

    def record(self):
        """ (None) -> None
        Turns camera on to capture video
        """
        print("Turning camera (adapterID: {}) on...".format(self.__adpater__))
        self.__capture__ = cv2.VideoCapture(self.__adpater__)

    def close(self):
        """ (None) -> None
        Turns camera off
        """
        print("Turning camera (adapterID: {}) off...".format(self.__adpater__))
        self.__capture__.release

    def __weight__(self, center, x):
        diff = x - center

        return -1**int(diff > 0) * (abs(diff) / center)

    def decodeQR(self, image):
        """ (cv2.image) -> list
        analyzes an image and returns info about all qr codes detected
        """
        decodedImage = pyzbar.decode(image)
        if (len(decodedImage) > 0):
            return decodedImage
        else:
            return []

    def findLines(self, img, color, angle=45):
        """ (cv2.image, int, tuple) -> list
        analyzes an image and detects lines within it
        """
        grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(img, (3,3), 3)
        edge = cv2.Canny(blur, self.__edgeThreshold1__, self.__edgeThreshold2__, apertureSize=3)
        line = cv2.HoughLines(edge, 1, np.pi / 180, self.__lineThreshold__)

        dim = img.shape
        height = dim[0]
        width  = dim[1]

        lines = list()

        if type(line) != type(None):
            for l in line:
                rho, theta = l[0]
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho

                x1 = int(x0 + 1000 * (-b))
                y1 = int(y0 + 1000 * a)
                x2 = int(x0 - 1000 * (-b))
                y2 = int(x0 - 1000 * a)

                avg_x  = (x2 + x1) // 2
                center = width // 2 
                cutoff = np.tan(np.deg2rad(angle))

                inv_slope = (x2 - x1) / ((y2 - y1) + 0.1e-09)
                if abs(inv_slope) < cutoff:
                    lines.append((x2 + x1)//2)
                    cv2.line(img, (x1,y1), (x2, y2), color, 2)

        return lines

    def analyze(self, img, mode, color):
        """ (cv2.image, int, int, tuple) -> tuple of list

        analyzes an image.
        reads qr codes, finds lines and displays image.
        +---------------------------------------------+
        |   mode = 0 : 000 : nothing                  |
        |   mode = 1 : 001 : decode qr                |
        |   mode = 2 : 010 : find lines               |
        |   mode = 3 : 011 : qr and line              |
        |   mode = 4 : 100 : display                  |
        |   mode = 5 : 101 : display and qr           |
        |   mode = 6 : 110 : display and line         |
        |   mode = 7 : 111 : display and qr and line  |
        +---------------------------------------------+ 
        """
        QR    = None
        Lines = None

        if mode & 0x1:
            QR = self.decodeQR(img)
        
        if mode & 0x2:
            Lines = self.findLines(img, color, angle=30)
        
        if mode & 0x4:
            dim = img.shape
            height = dim[0]
            width  = dim[1]
            center = width//2

            sum = 0
            avg = -1


            if Lines != None:
                for line in Lines:
                    sum += line
                
                if len(Lines):     
                    avg = sum / len(Lines)
                    cv2.line(img, (int(avg),0), (int(avg),height), (0,255,0), 2)

            #cv2.imshow("Image", cv2.Canny(cv2.blur(img, (3,3)), 250, 255))

            # draw center lines
            cv2.line(img, (center,0), (center,height), (255,0,0), 2)
            
            cv2.imshow("{}x{}".format(height, width), img)

        return QR, avg

    def readImg(self, img, mode, color):
        """ (cv2.image, int, int, tuple) -> None
        determines where the line is.
        """
        qr, lines  = self.analyze(img, mode, color)
        
        dimensions = img.shape
        height = dimensions[0]
        width = dimensions[1]

        sum = 0
        avg = -1

        if lines != None:
            for line in lines:
                sum += line
            
            if len(lines):     
                avg = sum / len(lines)
                cv2.line(img, (int(avg),0), (int(avg),height), (0,255,0), 2)

        return qr, avg

    def captureImage(self, mode, color=(0,0,255)):
        """ (int, int, int) -> None
        captures an image and analyzes it
        """
        _, frame = self.__capture__.read()
        qrCodes, avg = self.analyze(frame, mode, color)

        print("PID( {} )".format(avg))
        
        key = cv2.waitKey(1)
        if key == 27:
            return False
        return True
        
    def loadImage(self, filename, mode, color=(0,0,255)):
        """ (str, int, int, int) -> None
        loads an image and analyzes it
        """
        img = cv2.imread(filename)
        self.analyze(img, mode, color)

        cv2.waitKey(0)

def testLoad(cap, mode):
    print("Testing loading of image")

    filename = "LineFloor.jpg"
    #filename = "LineFloor2.jpg"

    if os.path.isfile(filename):
        cap.loadImage(filename, mode)
    else:
        print(filename, "is not a valid file.")

def testCap(cap, mode):
    print("Testing capture of images")
    cap.record()

    while(True):
        res = cap.captureImage(mode)
        if not res:
            break
    
    cap.close()


if __name__ == "__main__":
    cap = Capture(2, line_threshold=100, edge_threshold1=125, edge_threshold2=255, tolerance=1.1)
    testCap(cap,  cap.QR | cap.LINE | cap.DISPLAY)
    #testLoad(cap, cap.LINE | cap.DISPLAY)