from pyzbar.pyzbar import decode
import ImageCapture

CONFIG_FILE = r'c:\imagetesting\config.txt'
RESULT_FILE = r'c:\imagetesting\results.txt'

cam = ImageCapture.FsWebCam()

open(RESULT_FILE, 'w').close()

config = open(CONFIG_FILE, 'r')
results = open(RESULT_FILE, 'a+')

for index in range(1, 11):
    test = config.readline().split(' ', 1)
    img = cam.load(test[0])
    decodeString = cam.decode(img)
    if len(decodeString) > 0:
        if (test[1].replace('\n', '')) == decodeString[0].data.decode():
            results.write("test {}: passed\n".format(index))
        else:
            results.write("test {}: failed\n".format(index))
    else:
        results.write("test {}: failed to decode any QR codes\n".format(index))
        
results.close()
config.close()
