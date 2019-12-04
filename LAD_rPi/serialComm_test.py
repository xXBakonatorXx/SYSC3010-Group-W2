"""

Main LAD unit Raspberry Pi code.

developed by:
        Zachary Porter      : 101069001
        Erdem Yanikomeroglu : _________

Project Group : W2

"""
import ImageCapture
import PathFinding
import UDPSocket
import keyboard
import socket
import serial
import numpy
import json
import time

class Database:
    def __init__(self):
        self.data = dict()
        self.timestamp = 0

    def search(self, table, entry_val, byNumber=False):
        """ (str, str) -> dict
        
        Search the table for entry
        """

        for entry in self.data[table]:
            if byNumber:
                value = 'num'
            else:
                value = 'name'
            
            if entry[value] == entry_val:
                return entry
        return None

def LOG(data):
    print(type(data), data)

#macros
OP_MANUAL       = 0x400 # 0100 0000 0000
OP_AUTOMATIC    = 0x200 # 0010 0000 0000

DRV_FORWARD     = 0x100 # 0001 0000 0000
DRV_TURN_LEFT   = 0x080 # 0000 1000 0000
DRV_TURN_RIGHT  = 0x040 # 0000 0100 0000
MOV_ARM_UP      = 0x020 # 0000 0010 0000
MOV_ARM_DOWN    = 0x010 # 0000 0001 0000
MOV_WRIST_UP    = 0x008 # 0000 0000 1000
MOV_WRIST_DOWN  = 0x004 # 0000 0000 0100
MOV_HAND_OPEN   = 0x002 # 0000 0000 0010
MOV_HAND_CLOSE  = 0x001 # 0000 0000 0001

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
UDP_PORT       = 520
UDP_ENCODING   = 'utf-8'
UDP_TIMEOUT    = 1

# files to store camera image in
LOCATION_QR_FILE = 'locationQR.jpeg'
ITEM_QR          = 'itemQR.jpeg'

# table names
LOCATION_TABLE   = 'location'
ITEM_TABLE       = 'item'

# used to communicate with the arduino
# brannon set up comms between arduino and pi,
# he might remember the port to use.
SERIAL_PORT = 'COM4'

# used to store where lad came from (last_location)
# and next location (next_location)
last_location = 'home'
next_location = None
lad_location = 'home'

def create_map(graph):
    graph.addEdge(0, 1)
    graph.addEdge(1, 2) 
    graph.addEdge(1, 3) 
    graph.addEdge(3, 4)  

def get_turn(current_path, next_path, paths_list):
    """ (int, int, list of str) -> int

    Determines the direction the lad must turn when a QR code is found
    
    - paths_list    :   is a list of paths connecting to the intersection (paths from location table)
    - current_path  :   the index to the path the lad just came down, referances paths_list
    - next_path     :   the index to the path the lad must go down, referances paths_list

    paths_list = ["A", "B", "C", "D"]
      B
    A-|-C
      D

    <<<outputs>>>
    (-2)    :   turn around and take the same path your on
    (-1)    :   turn left
    (0)     :   go straight
    (1)     :   turn right

    >>> paths_list = ["a", "b", "c", "d"]
    >>> current_path = "a"
    >>> next_path = "b"
    >>> get_turn(current_path, next_path, paths_list)
    -1

    >>> paths_list = ["a", "b", "c", "d"]
    >>> current_path = "b"
    >>> next_path = "a"
    >>> get_turn(current_path, next_path, paths_list)
    1

    >>> paths_list = ["a", "b", "c", "d"]
    >>> current_path = "a"
    >>> next_path = "c"
    >>> get_turn(current_path, next_path, paths_list)
    0
    """

    current_idx = paths_list.index(current_path)
    next_idx    = paths_list.index(next_path)

    if (next_idx >= current_idx):
        turn = numpy.log2(2**next_idx//2**current_idx)
    else:
        turn = (-numpy.log2(2**current_idx//2**next_idx) + 2**2)

    return int(turn - 2)

def decode_server(server_data):
    """ (str)->(dict, int, string)
    
    Decodes data sent from server returns dictionary if json data is sent 
    or string if string is sent, or int if integer is sent 

    >>> decode_server('{"location": [{"name": "A", "pathA": "N"}, {"name": "B", "pathA": "N"}, {"name": "C", "pathA": "N"}, {"name": "D", "pathA": "N"}], "object": [{"name": "A", "location": "A"}, {"name": "B", "location": "B"}, {"name": "C", "location": "C"}, {"name": "D", "location": "D"}]}')
    {
        "location":[
            {"name": "A", "pathA": "N"},
            {"name": "B", "pathA": "N"},
            {"name": "C", "pathA": "N"}
        ]
        "items":[
            {"name": "A", "location": "A"},
            {"name": "B", "location": "B"},
            {"name": "C", "location": "C"},
            {"name": "D", "location": "D"}
        ]
    }

    >>> decode_server('item')
    'item'

    >>> decode_server(123)
    123
    """

    print("decoding server data {}".format(server_data))
    database_dict = dict()
    print("Trying to decode as json...")
    try:
        database_dict = json.loads(server_data)
    except:
        print("Decoding as string")
        return server_data

    return database_dict


def decode_arm_manual(arduino_op_code, up_code, down_code):
    if (arduino_op_code & up_code):
        return up_code
    elif (arduino_op_code & down_code):
        return down_code

def decode_arduino(camera, database, arduino_op_code, next_location):
    """ (camera obj, dict, int, int, list, int) -> int

    decodes the opcode from the arduino and performs some operations.

    """
    return_code = OP_AUTOMATIC

    if (arduino_op_code & OP_AUTOMATIC):

        if (arduino_op_code & LAD_SCAN_QR):
            # stop and take pic
            camera.capture('1280x720',LOCATION_QR_FILE,banner=False)
            img = camera.load(LOCATION_QR_FILE)

            #assuming 1 qr code for now
            qr_code = camera.decode(img)[0]
            entry = database.search(LOCATION_TABLE, qr_code.data.decode())
            
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

    elif (arduino_op_code & OP_MANUAL):
        # decode manual codes here.

        #move forward
        if (arduino_op_code & DRV_FORWARD):
            return_code |= DRV_FORWARD

            #turn left
            if (arduino_op_code & DRV_TURN_LEFT):
                return_code |= DRV_TURN_LEFT

            #turn right
            elif (arduino_op_code & DRV_TURN_RIGHT):
                return_code |= DRV_TURN_RIGHT
            
            #go straight
            elif (arduino_op_code & (DRV_TURN_LEFT & DRV_TURN_RIGHT)):
                return_code |= DRV_TURN_LEFT | DRV_TURN_RIGHT
        
        #move arm, wrist, hand
        return_code |= decode_arm_manual(arduino_op_code, MOV_ARM_UP, MOV_ARM_DOWN)
        return_code |= decode_arm_manual(arduino_op_code, MOV_WRIST_UP, MOV_WRIST_DOWN)
        return_code |= decode_arm_manual(arduino_op_code, MOV_HAND_OPEN, MOV_HAND_CLOSE)
        
    return return_code

def encode_arduino(ser, op_code):
    print("encoding arduino command")
    ser.write(op_code)

def find_path(graph, data):
    item = database.search(ITEM_TABLE, data)
    item_location = item['location']
    final_location = database.search(LOCATION_TABLE, item_location)
    final_location_idx = final_location['number']

    current_location = database.search(LOCATION_TABLE, lad_location)
    current_location_idx = current_location['number']

    path_map.findAllPaths(current_location_idx, final_location_idx)
    return path_map.getPath()


# main funciton
if __name__ == "__main__":
    #setup serial, udp client, camera, and database
    path_map = PathFinding.Graph(5)
    ser = serial.Serial(port=SERIAL_PORT,baudrate='9600')
    client = UDPSocket.Client(SERVER_ADDRESS, UDP_PORT, UDP_ENCODING, UDP_TIMEOUT)
    cap = ImageCapture.FsWebCam()
    database = Database()

    path2item = None
    
    res = OP_AUTOMATIC
    updated_data = False

    create_map(path_map)

    """ default values of server data, used to test diferent cases rn. will be over written by data read from server """
    server_data = "D_item"
    #server_data = str(OP_AUTOMATIC)
    #server_data = str(OP_MANUAL)
    #server_data = '{"location": [{"name": "A", "pathA": "N"}, {"name": "B", "pathA": "N"}, {"name": "C", "pathA": "N"}, {"name": "D", "pathA": "N"}], "object": [{"name": "A", "location": "A"}, {"name": "B", "location": "B"}, {"name": "C", "location": "C"}, {"name": "D", "location": "D"}]}'

    #debugg purpose
    database.data = json.load(open('test.json'))

    time.sleep(2)
    print('ready')

    while (not keyboard.is_pressed('esc')):
        # read from data base

        # read from server, if no new data after 1 sec the socket times out and server_data stays as its previous value.
        #server_data = client.receive()

        # decode server data
        last_data = data
        data = decode_server(server_data)

        if data != last_data:
            # flag that data has changed
            updated_data = True
        
        if (type(data) == type(dict())):
            # update database cache
            database.data = data
            database.timestamp = int(time.time())
            print("ts: {}, data keys: {}".format(database.timestamp, database.data.keys()))
        elif (type(data) == type(str())):
            print("referance database")
            #referance data base here

            if data != "cancel":
                if updated_data:
                    path2item = find_path(path_map, data)
                    print(path2item)
                else:
                    # continue last command
                    path2item = getPath(data)
                    for i in path2item:
                        nextLocation = path2item.pop
                        #go there
                        decode_arduino(cap, database, ser.write(0x010), nextLocation)
                        path2home.push(nextLocation)
            else:
                # return home
                for j in path2home:
                    nextLocation = path2home.pop
                    #go there
                    decode_arduino(cap, database, ser.write(0x010), nextLocation)

        elif (type(data) == type(int())):
            # encode arduino command
            if (data & OP_MANUAL):
                #send manual command
                encode_arduino(ser, 0x00)
                print("op code", hex(data))
            elif (data & OP_AUTOMATIC):
                # control loop send/receive

                #send OP_AUTOMATIC
                ser.write(res)

                #receive CODE
                arduino_op_code = ser.read_until(b'\n')

                #decode
                res = decode_arduino(cap, database, arduino_op_code, 'home')
                
                #send response
                x = 0

        time.sleep(2)

    print("Closing Serial connection to {}".format(ser.port))
    client.close()
    ser.close()
