# manual control test

from msvcrt import getch
import serial

OP_MANUAL = 0x800
OP_AUTOMA = 0x800
DRV_LFT_F = 0x100
DRV_LFT_R = 0x200
DRV_RHT_F = 0x080
DRV_RHT_R = 0x080
MOV_ARM_U = 0x010
MOV_ARM_D = 0x020
MOV_WST_U = 0x004
MOV_WST_D = 0x008
MOV_HND_O = 0x001
MOV_HND_C = 0x002

def encode(key):
    cmd = OP_MANUAL
    
    #arm
    if key == b'e':
        cmd |= MOV_ARM_U
    elif key == b'd':
        cmd |= MOV_ARM_D
        
    #wrist
    if key == b'r':
        cmd |= MOV_WST_U
    elif key == b'f':
        cmd |= MOV_WST_D
        
    return cmd


if __name__ == '__main__':
    ser = serial.Serial('com4', 9600)
    while (True):
        try:
            key = getch()
            cmd = str(encode(key)).encode()
            print(cmd)
            ser.write(cmd)
            res = ser.read_until(b'\n').decode()
            print(res)
        except Exception as err:
            print(type(err), err)
            break
    ser.close()