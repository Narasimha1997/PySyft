import numpy as np
import zmq
from random import choice

class FloatTensor():

    
    def __init__(self, controller, data, data_is_pointer = False, verbose=False):
        self.verbose = verbose
        self.controller = controller
        if(data is not None and not data_is_pointer):
            
            controller.socket.send_json({"functionCall":"createTensor", "data": list(data.flatten()), "shape": data.shape})
            
            self.id = int(controller.socket.recv_string())
        
            print("FloatTensor.__init__: " +  str(self.id))

        elif(data_is_pointer):
            self.id = int(data)


    def __add__(self,x):

        self.controller.socket.send_json(self.cmd("add",[x.id])) # sends the command
        return FloatTensor(self.controller,int(self.controller.socket.recv_string()),True)

        return "Tensors don't have the same shape"

    
    def abs(self):

        self.controller.socket.send_json(self.cmd("abs")) # sends the command
        res = self.controller.socket.recv_string() # receives output from command

        if(self.verbose):
            print(res)

        return self

    def neg(self):

        self.controller.socket.send_json(self.cmd("neg")) # sends the command
        return self.controller.socket.recv_string() # receives output from command

    
    def __repr__(self):
        self.controller.socket.send_json({"functionCall":"print","objectType":"tensor","objectIndex":self.id})
        res = self.controller.socket.recv_string() # receives output from command
        
        return res

    def __str__(self):
        self.controller.socket.send_json({"functionCall":"print","objectType":"tensor","objectIndex":self.id})
        return self.controller.socket.recv_string()

    def print(self):

        self.controller.socket.send_json({"functionCall":"print","objectType":"tensor","objectIndex":self.id})
        res = self.controller.socket.recv_string() # receives output from command

        return res

    def cmd(self,functionCall,tensorIndexParams=[]):
        cmd = {}
        cmd['functionCall'] = functionCall
        cmd['objectType'] = 'tensor'
        cmd['objectIndex'] = self.id
        cmd['tensorIndexParams'] = tensorIndexParams
        return cmd

    def print(self):
        self.controller.socket.send_json({"functionCall":"print","objectType":"tensor","objectIndex":self.id})
        
        print(self.controller.socket.recv_string())


class SyftController():

    def __init__(self, identity):

        self.identity = identity

        context = zmq.Context()
        self.socket = context.socket(zmq.DEALER)
        self.socket.setsockopt_string(zmq.IDENTITY, identity)
        self.socket.connect("tcp://localhost:5555")

    def FloatTensor(self,data):
        return FloatTensor(self,data)
