from firebase import firebase
import serial
import re
import time
from threading import Thread
import asyncio
from websocket import create_connection

firebase = firebase.FirebaseApplication('https://ariot2016.firebaseio.com', authentication=None)

buffer = [1000, 1000, 1000, 1000, 1000, 1000]

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
	if(len(line)==0):
		return False
	elif(line[0]=='[' and line[len(line)-1]==']'):
		print("valid")
		return True


ws = create_connection('ws://10.59.10.2:5000/indianadrones')
websocket.send(buffer)
print("websocket ok");
		
		
ser = serial.Serial('/dev/ttyUSB0', 9600)

thread = Thread(target=background_thread)
thread.daemon = True
thread.start()
asyncio.get_event_loop().run_until_complete(hello())

while 1:
	line = ser.readline()
	line = line.decode('unicode_escape', errors='ignore')
	if(validateLine(line)):
		line = re.search("(\[[0-9, ]+\])", line).group()
		buffer = eval(line)
		#result = firebase.post('/distance', 'distance_data: { right: ' + str(buffer[0]) + ', left: ' + str(buffer[1]) + ', top: ' + str(buffer[2]) + ', bottom: ' + str(buffer[3]) + ', front: ' + str(buffer[4]) + ', bottom: ' + str(buffer[5]) + '}')
		



