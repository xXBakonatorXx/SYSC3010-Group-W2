import os
import sys
import subprocess 
try:
    import pyzbar.pyzbar as pyzbar
    from PIL import Image
except Exception as e:
    print(type(e), e)

class FsWebCam:
    def __init__(self):
        x = 0

    def capture(self, resolution, filename, banner=False):
        banner_s = "--no-banner"
        if banner:
            banner_s = ""
        try:
            proc = subprocess.Popen(['fswebcam', '-r', resolution, banner_s, filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = proc.communicate()
        except Exception as e:
            print(type(e), e)

    def load(self, filename):
        return Image.open(filename)

    def decode(self, image):
        return pyzbar.decode(image)

if __name__ == "__main__":
    cam = FsWebCam()
    filename = "testFS.jpeg"
    cam.capture("1280x720", filename, banner=False)
    img = cam.load(filename)
    cam.decode(img)