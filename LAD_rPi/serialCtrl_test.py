import keyboard
import serial
import time

#macros
OP_MANUAL = 0x800 # 1000 0000 0000
OP_AUTOMA = 0x400 # 0100 0000 0000
DRV_LFT_F = 0x100 # 0001 0000 0000
DRV_LFT_R = 0x200 # 0010 0000 0000
DRV_RHT_F = 0x040 # 0000 0100 0000
DRV_RHT_R = 0x080 # 0000 1000 0000
MOV_ARM_U = 0x010 # 0000 0001 0000
MOV_ARM_D = 0x020 # 0000 0010 0000
MOV_WST_U = 0x004 # 0000 0000 0100
MOV_WST_D = 0x008 # 0000 0000 1000
MOV_HND_O = 0x001 # 0000 0000 0001
MOV_HND_C = 0x002 # 0000 0000 0010

LAD_LINE        =  0x000 # 0000 0000 0000
LAD_FORWARD     =  0x002 # 0000 0000 0010
LAD_TURN_LEFT   =  0x008 # 0000 0000 1000
LAD_TRUN_RIGHT  =  0x001 # 0000 0000 0001
LAD_TURN_AROUND =  0x004 # 0000 0000 0100
LAD_NO_LINE     =  0x010 # 0000 0001 0000
LAD_ALL_LINE    =  0x01F # 0000 0001 1111
LAD_STOP        =  0x020 # 0000 0010 0000
LAD_CONTINUE    =  0x00F # 0000 0000 1111

SER_BUF = 5

time_step = .05

def send(cmd):
    return cmd

def decode(cmd, arm_pos, wrist_pos, hand_pos):
    mtr_l_spd = 100
    mtr_l_dir = 0
    mtr_r_spd = 100
    mtr_r_dir = 0

    motor_step = 0.25
    arm_max = 45
    arm_min = 0
    wrist_max = 15
    wrist_min = -15
    hand_max = 10
    hand_min = 0

    if (cmd & DRV_LFT_F):
        mtr_l_dir = 1
    elif (cmd & DRV_LFT_R):
        mtr_l_dir = -1

    if (cmd & DRV_RHT_F):
        mtr_r_dir = 1
    elif (cmd & DRV_RHT_R):
        mtr_r_dir = -1

    if (cmd & MOV_ARM_U):
        if (arm_pos < arm_max):
            arm_pos += motor_step
        else: 
            arm_pos = arm_max
    elif (cmd & MOV_ARM_D):
        if (arm_pos > arm_min):
            arm_pos -= motor_step
        else:
            arm_pos = arm_min

    if (cmd & MOV_WST_U):
        if (wrist_pos < wrist_max):
            wrist_pos += motor_step
        else: 
            wrist_pos = wrist_max
    elif (cmd & MOV_WST_D):
        if (wrist_pos > wrist_min):
            wrist_pos -= motor_step
        else:
            wrist_pos = wrist_min

    if (cmd & MOV_HND_O):
        if (hand_pos < hand_max):
            hand_pos += motor_step
        else: 
            hand_pos = hand_max
    elif (cmd & MOV_HND_C):
        if (hand_pos > hand_min):
            hand_pos -= motor_step
        else:
            hand_pos = hand_min

    print("Left dir: {}, Right dir {}, Arm position: {}', Wrist position {}', Hand position {}'".format(mtr_l_dir, mtr_r_dir, arm_pos, wrist_pos, hand_pos))
    return arm_pos, wrist_pos, hand_pos

arm_pos = 0
wrist_pos = 0
hand_pos = 0

while (True):
    cmd = OP_MANUAL
    try:
        if keyboard.is_pressed("q"):
            cmd |= DRV_LFT_F

        if keyboard.is_pressed("a"):
            cmd |= DRV_LFT_R
        
        if keyboard.is_pressed("w"):
            cmd |= DRV_RHT_F
        
        if keyboard.is_pressed("s"):
            cmd |= DRV_RHT_R
        
        if keyboard.is_pressed("e"):
            cmd |= MOV_ARM_U
        
        if keyboard.is_pressed("d"):
            cmd |= MOV_ARM_D
        
        if keyboard.is_pressed("r"):
            cmd |= MOV_WST_U
        
        if keyboard.is_pressed("f"):
            cmd |= MOV_WST_D
        
        if keyboard.is_pressed("o"):
            cmd |= MOV_HND_O
        
        if keyboard.is_pressed("p"):
            cmd |= MOV_HND_C
        
        if keyboard.is_pressed("enter"):
            break
    except:
        break
    print("Command encoding: {}".format(hex(cmd)))
    arm_pos, wrist_pos, hand_pos = decode(cmd, arm_pos, wrist_pos, hand_pos)
    print()
    time.sleep(time_step)