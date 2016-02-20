from socketIO_client import SocketIO, BaseNamespace, LoggingNamespace
import time


# with SocketIO('localhost', 5000, LoggingNamespace) as socketIO:
#     socketIO.emit('test')
#     socketIO.wait(seconds=1)

class IndianaDronesNamespace(BaseNamespace):

    def on_connect(self):
        print('[Connected]')
        self.emit("test")

    def on_test_response(self, *args):
        print("Takeoff")
        print(args)
        # socketIO.wait(milliseconds=500)
        time.sleep(0.5)
        self.emit('test')


socketIO = SocketIO('localhost', 5000)
indy = socketIO.define(IndianaDronesNamespace, '/indy')

# indy.emit('test')
# socketIO.wait(seconds=1)


# socketIO = SocketIO('localhost', 5000)
# with socketIO.define(IndianaDronesNamespace, '/lol'):
#     socketIO.emit("test")
#     socketIO.wait(seconds=1)


# time.sleep(10)
