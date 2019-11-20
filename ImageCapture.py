import os
import subprocess
import sys
try:
    import pyzbar.pyzbar as pyzbar
    from PIL import Image
except Exception as e:
    print(type(e), e)

class FsWebCamError(Exception):
    def init(self, error):
        print(error)

class FsWebCam:
    def __init__(self):
        print("Starting camera...")

    def capture(self, resolution, filename, banner=False):
        banner_s = "--no-banner"
        if banner:
            banner_s = ""
        try:
            res = os.system('fswebcam -r {} {} {}'.format(resolution, banner_s, filename))
            if res == 0:
                raise FsWebCamError("fswebcam failed to run")
            
        except Exception as e:
            print(type(e), e)

    def __x_capture__(self, resolution, filename, banner=False):
        banner_s = "--no-banner"
        if banner:
            banner_s = ""
        try:
            p = subprocess.Popen(['fswebcam', '-r', resolution, banner_s, filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()
            if err != b'':
                raise FsWebCamError(err.decode('utf-8'))
            
        except Exception as e:
            print(type(e), e)

    def load(self, filename):
        return Image.open(filename)

    def decode(self, image):
        return pyzbar.decode(image)#, symbols=[pyzbar.ZBarSymbol.QRCODE])

if __name__ == "__main__":
    cam = FsWebCam()
    filename = "testFS.jpeg"
    cam.capture("1280x720", filename, banner=False)
    img = cam.load(filename)
    cam.decode(img)
