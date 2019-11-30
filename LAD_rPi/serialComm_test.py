import ImageCapture
import UDPSocket
import keyboard
import serial
import numpy
import json
import time

class Database:
    def __init__(self):
        self.data = dict()
        self.timestamp = 0

    def search(self, table, entry_name):
        for entry in self.data[table]:
            if entry['name'] == entry_name:
                return entry
        return None

def LOG(data):
    print(type(data), data)

#macros
OP_MANUAL       = 0x400 # 0100 0000 0000
OP_AUTOMATIC    = 0x200 # 0010 0000 0000

DRV_FORWARD     = 0x100 # 0001 0000 0000
FLAG_TURN_LEFT  = 0x080 # 0000 1000 0000
FLAG_TURN_RIGHT = 0x040 # 0000 0100 0000
MOV_ARM_UP      = 0x020 # 0000 0010 0000
MOV_ARM_DOWN    = 0x010 # 0000 0001 0000
MOV_WST_UP      = 0x008 # 0000 0000 1000
MOV_WST_DOWN    = 0x004 # 0000 0000 0100
MOV_HND_OPEN    = 0x002 # 0000 0000 0010
MOV_HND_CLOSE   = 0x001 # 0000 0000 0001

LAD_X           = 0x100 # 0001 0000 0000
LAD_XX          = 0x080 # 0000 1000 0000
LAD_XXX         = 0x040 # 0000 0000 0001

LAD_SCAN_QR     = 0x020 # 0000 0100 0000
LAD_DRIVE       = 0x010 # 0000 0010 0000
LAD_TURN        = 0x008 # 0000 0001 0000
LAD_DIRECTION   = 0x004 # 0000 0000 1000
LAD_MOV_ARM     = 0x002 # 0000 0000 0100
LAD_NO_LINE     = 0x001 # 0000 0000 0010

SERVER_ADDRESS = '127.0.0.1'
UDP_PORT = 520

SERIAL_PORT = 'COM4'

last_location = 'home'

def get_turn(current_path, next_path, paths_list):
    current_idx = paths_list.index(current_path)
    next_idx    = paths_list.index(next_path)

    if (next >= curr):
        turn = numpy.log2(2**next_idx//2**current_idx)
    else:
        turn = (-numpy.log2(2**current_idx//2**next_idx) + 2**2)

    return int(turn - 2)

def decode_server(server_data):
    print("decoding server data {}".format(server_data))
    database_dict = dict()
    print("Trying to decode as json...")
    database_dict = json.loads(server_data)

    try:
        keys = database_dict.keys()
        return database_dict
    except:
        return int(database_dict)

def decode_arduino(camera, database, arduino_op_code, command_list, command_idx):
    return_code = OP_AUTOMATIC

    next_location = command_list[command_idx]

    if (arduino_op_code & OP_AUTOMATIC):

        if (arduino_op_code & LAD_SCAN_QR):
            # stop and take pic
            filename = 'locationQR.jpeg'
            tablename = 'location'
            camera.capture('1280x720',filename,banner=False)
            img = camera.load(filename)

            #assuming 1 qr code for now
            qr_code = camera.decode(img)[0]
            entry = database.search(tablename, qr_code.data.decode())
            
            if entry == None:
                return -1

            entry_data = list()
            entry_name = entry['name']
            entry_data.append(entry['pathA'])
            entry_data.append(entry['pathB'])
            entry_data.append(entry['pathC'])
            entry_data.append(entry['pathD'])

            # determine turn.
            turn_direction = get_turn(last_location, next_location, entry_data)
            last_location = next_location
            
            if turn_direction == 0:
                # flag go straight
                return_code |= LAD_DRIVE

            elif turn_direction == 1:
                # flag go left
                return_code |= LAD_TURN

            elif turn_direction == -1:
                # flag go right
                return_code |= LAD_TURN | LAD_DIRECTION

            else:
                # flag go back
                return_code |= LAD_DRIVE | LAD_DIRECTION

        # decode steering command
        elif (arduino_op_code & LAD_DRIVE):
            if (arduino_op_code & LAD_DIRECTION):
                # turn around
                return_code |= LAD_DRIVE | LAD_DIRECTION

            else:
                # straight
                return_code |= LAD_DRIVE

        elif (arduino_op_code & LAD_TURN):
            if (arduino_op_code & LAD_DIRECTION):
                # turn right
                return_code |= LAD_TURN | LAD_DIRECTION

            else:
                # turn left
                return_code |= LAD_TURN

        elif (arduino_op_code & LAD_MOV_ARM):
            # move arm routine
            return_code |= LAD_MOV_ARM

        elif (arduino_op_code & LAD_NO_LINE):
            # fallen off line
            return_code |= LAD_NO_LINE

        elif (arduino_op_code & LAD_ALL_LINE):
            # all sensors see a line
            return_code |= LAD_ALL_LINE
        
    return return_code

def encode_arduino(ser):
    print("encoding arduino command")
    arduino_cmd = 0x0
    ser.write(arduino_cmd)

if __name__ == "__main__":
    ser = serial.Serial(port=SERIAL_PORT,baudrate='9600')
    client = UDPSocket.Client(SERVER_ADDRESS, UDP_PORT)
    cap = ImageCapture.FsWebCam()

    database = Database()
    res = OP_AUTOMATIC

    server_data = str(OP_AUTOMATIC)
    #server_data = str(OP_MANUAL)
    #server_data = '{"location": [{"name": "A", "pathA": "N"}, {"name": "B", "pathA": "N"}, {"name": "C", "pathA": "N"}, {"name": "D", "pathA": "N"}], "object": [{"name": "A", "location": "A"}, {"name": "B", "location": "B"}, {"name": "C", "location": "C"}, {"name": "D", "location": "D"}]}'

    time.sleep(2)
    print('ready')

    while (not keyboard.is_pressed('esc')):
        # read from data base
        #server_data = client.receive()

        # decode server data
        data = decode_server(server_data)   
        
        if type(data) == type(dict()):
            # update database cache
            database.data = data
            database.timestamp = int(time.time())
            print("ts: {}, data keys: {}".format(database.timestamp, database.data.keys()))
        else:
            # encode arduino command
            if (data & OP_MANUAL):
                #send manual command
                encode_arduino(ser)
                print("op code", hex(data))
            elif (data & OP_AUTOMATIC):
                # control loop send/receive

                #send OP_AUTOMATIC
                ser.write(res)

                #receive CODE
                arduino_op_code = ser.read_until(b'\n')

                #decode
                res = decode_arduino(cap, database, arduino_op_code, ['home'], 0)
                
                #send response
                x = 0

        time.sleep(2)

    print("Closing Serial connection to {}".format(ser.port))
    client.close()
    ser.close()
