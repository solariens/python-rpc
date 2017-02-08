#!-*-coding:utf-8-*-

import pickle
from multiprocessing.connection import Listener
import threading

class RPCHandler(object):

    def __init__(self, address, port, authkey):
        self._functions = {}
        self._fd = 0
        self.address = (address, port)
        self.authkey = authkey

    def setServerFd(self):
        self._fd = Listener(self.address, authkey=self.authkey)

    def registerFunc(self, func):
        self._functions[func.__name__] = func

    def handlerRecv(self, connection):
        try:
            while True:
                func, args, kwargs = pickle.loads(connection.recv())
                try:
                    result = self._functions[func](*args, **kwargs)
                    connection.send(pickle.dumps(result))
                except Exception as e:
                    connection.send(pickle.dumps(e))
        except EOFError:
            pass

    def recieveFunc(self):
        while True:
            client = self._fd.accept()
            t = threading.Thread(target=self.handlerRecv, args=(client,))
            t.daemon = True
            t.start()

    def run(self):
        self.setServerFd()
        self.recieveFunc()

def add(a, b):
    return a + b

if __name__ == '__main__':
    rpc = RPCHandler('localhost', 8888, 'solariens')
    rpc.registerFunc(add)
    rpc.run()
