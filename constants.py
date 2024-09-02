BLOCK = 1 
BLOCKCHAIN = 2 
TRANSACTION = 3
ACCESS = 4 
INFO = 5

from datetime import datetime
import time
import socket

class Transaction:
    def __init__(self, index=None):
        if not index:
            self.index = int(1000*time.time())
        else:
            self.index = index
    def __str__(self):
        return f"Transaction #{self.index}"
    
class Message:
    def __init__(self,messagebody,type,isBroadcast = False,numSign = 0):
        self.messagebody = messagebody
        self.type = type
        self.messageid = int(1000*time.time())
        self.isBroadcast = isBroadcast
        self.numSign = numSign
    
    def getMessageBody(self):
        return self.messagebody
    def __str__(self):
        return f"{self.messagebody}:{self.type}:{self.isBroadcast}:{self.messageid}:{self.numSign}"

    # @classmethod
    # def from_string(cls, string):
        
class Block:
    def __init__(self, index):
        self.index = index

    @staticmethod
    def create_genesis_block():
        # Manually create the first block (genesis block)
        return Block(0)

    def __str__(self):
        return f"Block #{self.index}"