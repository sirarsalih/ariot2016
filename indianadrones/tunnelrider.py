from firebase import firebase
import serial
import re
import time
from threading import Thread
from socketIO_client import SocketIO, BaseNamespace, LoggingNamespace
import time


firebase = firebase.FirebaseApplication('https://ariot2016.firebaseio.com', authentication=None)

dist_buf = [1000, 1000, 1000, 1000, 1000, 1000]

MOCK = True


def background_thread():
    while True:
        time.sleep(1)
        result = firebase.post('/distance', 'distance_data: { right: ' + str(dist_buf[0]) + ', left: ' + str(dist_buf[1]) + ', top: ' + str(dist_buf[2]) + ', bottom: ' + str(dist_buf[3]) + ', front: ' + str(dist_buf[4]) + ', bottom: ' + str(dist_buf[5]) + '}')
        print(result)


def validateLine(line):

    line = line.rstrip('\r\n')
    if len(line) is 0:
        return False
    elif line[0] == '[' and line[len(line)-1] == ']':
        print("valid")
        return True


def shouldFly():
    (x, y, z) = (0, 0, 0)
    # 1. if drone is too close to roof, it should move down.
    # Then no if distance is over 12 cm no need.
    if dist_buf[2] > 0 and dist_buf[2] < 12:
        y = -1
    else:
        y = 0
    # 2. Under 12 cm from right wall, fly away from it. Over 50 cm,
    if dist_buf[0] > 0 and dist_buf[0] < 25:
        x = -1
    elif dist_buf[0] > 100 and dist_buf[0] < 1000:
        x = 1
    else:
        x = 0
    # Front is facing obstacle below 40 cm. GO BACK!
    if dist_buf[4] > 0 and dist_buf[4] < 40:
        z = -1
    else:
        z = 1

    return (x, y, z)


if not MOCK:
    ser = serial.Serial('/dev/ttyUSB0', 9600)


class IndianaDronesNamespace(BaseNamespace):

    def on_connect(self):
        print('[Connected]')
        # self.emit("test")
        self.emit("indy takeoff")

    def on_test_response(self, *args):
        print(args)
        time.sleep(0.5)
        self.emit('test')

    def on_indy_response(self, *args):
        global ser
        global dist_buf
        print(args)
        time.sleep(0.5)

        (x, y, z) = shouldFly()

        if not MOCK:
            line = ser.readline()
            line = line.decode('unicode_escape', errors='ignore')
            if validateLine(line):
                line = re.search("(\[[0-9, ]+\])", line).group()
                dist_buf = eval(line)

        self.move_z(z)
        self.move_x(x)
        self.move_y(y)

    def move_z(self, z):
        if z > 0:
            self.emit('indy forward')
        elif z < 0:
            self.emit('indy backward')

    def move_x(self, x):
        if x > 0:
            self.emit('indy right')
        elif x < 0:
            self.emit('indy left')

    def move_y(self, y):
        if y > 0:
            self.emit('indy up')
        elif y < 0:
            self.emit('indy down')


socketIO = SocketIO('localhost', 4000)
indy = socketIO.define(IndianaDronesNamespace, '/indianadrones')


# if not MOCK:
#     ser = serial.Serial('/dev/ttyUSB0', 9600)

#     thread = Thread(target=background_thread)
#     thread.daemon = True
#     thread.start()

#     while True:
#         line = ser.readline()
#         line = line.decode('unicode_escape', errors='ignore')
#         if validateLine(line):
#             line = re.search("(\[[0-9, ]+\])", line).group()
#             dist_buf = eval(line)
