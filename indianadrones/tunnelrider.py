from firebase import firebase
import serial
import re
import time
from threading import Thread

firebase = firebase.FirebaseApplication('https://ariot2016.firebaseio.com', authentication=None)

buffer = [1000, 1000, 1000, 1000, 1000, 1000]

MOCK = True


def background_thread():
    while True:
        time.sleep(1)
        result = firebase.post('/distance', 'distance_data: { right: ' + str(buffer[0]) + ', left: ' + str(buffer[1]) + ', top: ' + str(buffer[2]) + ', bottom: ' + str(buffer[3]) + ', front: ' + str(buffer[4]) + ', bottom: ' + str(buffer[5]) + '}')
        print(result)


def matchRegex(line):
    if(1):
        return True
    else:
        return False


def validateLine(line):

    line = line.rstrip('\r\n')
    if len(line) is 0:
        return False
    elif line[0] == '[' and line[len(line)-1] == ']':
        print("valid")
        return True


def shouldFly():
    x, y, z = 0
    # 1. if drone is too close to roof, it should move down.
    # Then no if distance is over 12 cm no need.
    if buffer[2] > 0 and buffer[2] < 12:
        y = -1
    else:
        y = 0
    # 2. Under 12 cm from right wall, fly away from it. Over 50 cm,
    if buffer[0] > 0 and buffer[0] < 25:
        x = -1
    elif buffer[0] > 100 and buffer[0] < 1000:
        x = 1
    else:
        x = 0
    # Front is facing obstacle below 40 cm. GO BACK!
    if buffer[4] > 0 and buffer[4] < 40:
        z = -1
    else:
        z = 1

    return (x, y, z)


if not MOCK:
    ser = serial.Serial('/dev/ttyUSB0', 9600)

    thread = Thread(target=background_thread)
    thread.daemon = True
    thread.start()

    while True:
        line = ser.readline()
        line = line.decode('unicode_escape', errors='ignore')
        if(validateLine(line)):
            line = re.search("(\[[0-9, ]+\])", line).group()
            buffer = eval(line)
