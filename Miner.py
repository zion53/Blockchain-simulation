from node_final import Node
from constants import *
import hashlib

class Miner (Node):

    # Python class constructor
    def __init__(self, host, port, id=None, hash_chain=[], transactionpool =[], callback=None, max_connections=5):
        super(Miner, self).__init__(host, port, id, callback, max_connections)
        print("\033[92mMiner: Started\033[0m")
        self.hash_chain = hash_chain 
        self.transactionpool = transactionpool
            
    def receive_chain(self, chain_string):
        # Parse the chain string and create block objects
        blocks_data = chain_string.strip().split('\n')
        self.hash_chain = []
        for block_data in blocks_data:
            block_hash = hashlib.sha256(block_data.encode()).hexdigest()
            self.hash_chain.append(block_hash)
    
    def add_to_transaction_pool(self, transaction):
        self.transactionpool.append(transaction)
            
    def print_transaction_pool(self):
        # ANSI escape code for green color
        green_color_code = "\033[92m"
        reset_color_code = "\033[0m"
        print("\n")
        print(green_color_code + "Transaction Pool" + reset_color_code)
        for transaction in self.transactionpool:
            print(green_color_code + str(transaction) + reset_color_code)
        print("\n")
            
    def display_chain(self):
        for i, block in enumerate(self.hash_chain):
            print(f"Block {i + 1} hash: {block}")
            
    
    def receive_data(self, transaction_string, rec_type):
        index = int(transaction_string.split('#')[1].strip())        
        if(int(rec_type) == TRANSACTION):
            transaction = Transaction(index)
            self.transactionpool.append(transaction)
        elif(int(rec_type) == BLOCK):
            block = Block(index)
            block_data = str(block)
            block_hash = hashlib.sha256(block_data.encode()).hexdigest()
            self.hash_chain.append(block_hash)
            
    def add_block(self, block):
            block_data = str(block)
            block_hash = hashlib.sha256(block_data.encode()).hexdigest()
            self.hash_chain.append(block_hash)

    def outbound_node_connected(self, node):
        print(f"\033[92moutbound_node_connected : {node.host}:{node.port} \033[0m")

    def inbound_node_connected(self, node):
        print(f"\033[92minbound_node_connected : {node.host}:{node.port} \033[0m")

    def inbound_node_disconnected(self, node):
        print(f"\033[92minbound_node_disconnected : {node.host}:{node.port} \033[0m")

    def outbound_node_disconnected(self, node):
        print(f"\033[92moutbound_node_disconnected : {node.host}:{node.port} \033[0m")



    def node_message(self, node, data):
        """This method is invoked when a node send us a message.
            data is a string, need to convert to a message object
        """
        """ for miner It will ignore if some one request some data from it """
        
        self.debug_print("node_message: " + node.id + ": " + str(data))
        # print(data)
        parts = str(data).split(":")
        messagebody = parts[0]
        type = parts[1]
        isBroadcast = parts[2]
        message_id = int(parts[3])
        num_sign = int(parts[4])

        if int(type) == BLOCKCHAIN: 
            self.receive_chain(messagebody)
            self.display_chain()
        elif int(type) == TRANSACTION:
            self.receive_data(messagebody,type)
            print("\033[92mTransaction received from " + node.host + ":" + str(node.port) + "\033[0m")
            print(messagebody)
            print("\n")
        elif int(type) == BLOCK:
            self.receive_data(messagebody,type)
            print("\033[92mBlock received from " + node.host + ":" + str(node.port) + "\033[0m")
            print(messagebody)
            print("\n")
        elif int(type) == ACCESS:
            self.send_to_node(node ,Message("I am not a full node", INFO , False, 0))
        elif int(type) == INFO:
            print("\033[93mMessage received from " + node.host + ":" + str(node.port) + "\033[0m")
            print(messagebody)
            print("\n")

        if isBroadcast == "True":
            if message_id not in self.broadcasted_messages:
                self.broadcasted_messages.add(message_id)
                self.send_to_nodes(data, exclude=[node])
        
    def node_disconnect_with_outbound_node(self, node):
        print("\033[92mnode wants to disconnect with other outbound node:" + node.id + "\033[0m")

    def node_request_to_stop(self):
        print("\033[92mnode is requested to stop\033[0m")

