from node_final import Node
from constants import *
import hashlib

class LightNode (Node):

    # Python class constructor
    def __init__(self, host, port, id=None, chain=[], callback=None, max_connections=5):
        super(LightNode, self).__init__(host, port, id, callback, max_connections)
        self.chain = chain 
        print("\033[93mLight Node: Started\033[0m")

    def receive_chain(self, chain_string):
        # Parse the chain string and create block objects
        blocks_data = chain_string.strip().split('\n')
        self.chain = []
        for block_data in blocks_data:
            block_hash = hashlib.sha256(block_data.encode()).hexdigest()
            self.chain.append(block_hash)

    def receive_data(self, transaction_string, rec_type):
        index = int(transaction_string.split('#')[1].strip())

        if(rec_type == BLOCK):
            block = str(Block(index))
            block_hash = hashlib.sha256(block.encode()).hexdigest()
            self.chain.append(block_hash)

    def node_message(self, node, data):
        """This method is invoked when a node send us a message.
            data is a string, need to convert to a message object
        """
        # self.debug_print("node_message: " + node.id + ": " + str(data))
        parts = str(data).split(":")
        messagebody = parts[0]
        type = int(parts[1])
        isBroadcast = parts[2]
        message_id = parts[3]
        num_sign = int(parts[4])
        
        if type == BLOCKCHAIN: 
            self.receive_chain(chain_string = messagebody)
            self.display_chain()
        elif type == BLOCK:
            self.receive_data(messagebody,type)
            print("\033[93mBlock received from " + node.host + ":" + str(node.port) + "\033[0m")
            print(messagebody)
            print("\n")
        elif type == ACCESS:
            self.send_to_node(node ,Message("I am not a full node", INFO , False, 0))
        elif type == INFO:
            print("\033[93mMessage received from " + node.host + ":" + str(node.port) + "\033[0m")
            print(messagebody)
            print("\n")

        if isBroadcast:
            if message_id not in self.broadcasted_messages:
                self.broadcasted_messages.add(message_id)
                self.send_to_nodes(data, exclude=[node])
            

    def display_chain(self):
        for i, block in enumerate(self.chain):
            print("\033[93mBlock {} hash: {}\033[0m".format(i + 1, block))

    def outbound_node_connected(self, node):
        print("\033[93moutbound_node_connected {}: {}\033[0m".format(node.host, node.port))

    def inbound_node_connected(self, node):
        print("\033[93minbound_node_connected: {}: {}\033[0m".format(node.host, node.port))

    def inbound_node_disconnected(self, node):
        print("\033[93minbound_node_disconnected: {}: {}\033[0m".format(node.host, node.port))

    def outbound_node_disconnected(self, node):
        print("\033[93moutbound_node_disconnected: {}: {}\033[0m".format(node.host, node.port))

    def node_disconnect_with_outbound_node(self, node):
        print("\033[93mnode wants to disconnect with other outbound node: {}: {}\033[0m".format(node.host, node.port))

    def node_request_to_stop(self):
        print("\033[93mnode is requested to stop ({}):\033[0m".format(self.id))
