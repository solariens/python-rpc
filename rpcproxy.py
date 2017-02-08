#!-*-coding:utf-8-*-

import pickle
from multiprocessing.connection import Client

class RPCProxy(object):
    def __init__(self, address, port, authkey):
        self._connection = Client((address, port), authkey=authkey)

    def __getattr__(self, name):
        def do_rpc(*args, **kwargs):
            self._connection.send(pickle.dumps((name, args, kwargs)))
            result = pickle.loads(self._connection.recv())
            if isinstance(result, Exception):
                raise result
            return result
        return do_rpc

if __name__ == '__main__':
    proxy = RPCProxy('localhost', 8888, 'solariens')
    print(proxy.add(1, 2))
