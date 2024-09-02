from node_final import Node
from constants import *

class FullNode (Node):

    # Python class constructor
    def __init__(self, host, port, id=None, chain=[], callback=None, max_connections=5):
        super(FullNode, self).__init__(host, port, id, callback, max_connections)
        self.chain = chain 
        print("\033[94mFull Node Started\033[0m")


    def receive_chain(self, chain_string):
        # Parse the chain string and create block objects
        blocks_data = chain_string.strip().split('\n')
        self.chain = []
        for block_data in blocks_data:
            index = int(block_data.split('#')[1].strip())
            block = Block(index)
            self.chain.append(block)

    def display_chain(self):
        for block in self.chain:
            print(block)

    def get_chain_string(self):
        chain_string = ""
        for block in self.chain:
            chain_string += str(block) + "\n"
        return chain_string
    

    def receive_data(self, transaction_string, rec_type):
        
        index = int(transaction_string.split('#')[1].strip())
        if(int(rec_type) == BLOCK):
            block = Block(index)
            self.chain.append(block)


    def node_message(self, node, data):
        """This method is invoked when a node send us a message.
            data is a string, need to convert to a message object
        """
        # self.debug_print("node_message: " + node.id + ": " + str(data))
        # print(data)
        parts = str(data).split(":")
        messagebody = parts[0]
        type = parts[1]
        isBroadcast = parts[2]
        message_id = int(parts[3])
        num_sign = int(parts[4])

        # print("Message Structure starts")
        # print(messagebody)
        # print(type)
        # print(isBroadcast)
        # print(message_id)
        # print("Message Structure ends")
        
        if int(type) == BLOCKCHAIN: 
            self.receive_chain(messagebody)
            self.display_chain()
        elif int(type) == BLOCK:
            self.receive_data(messagebody,type)
            print("\033[94mBlock received from " + node.host + ":" + str(node.port) + "\033[0m")
            print(messagebody)
            print("\n")
        elif int(type) == ACCESS:
            self.send_to_node(node, Message(self.get_chain_string(), BLOCKCHAIN , False, 0))
            print("Blockchain sent to node : " + node.host + " : " + str(node.port))
            print("\n")

        if isBroadcast == "True":
            if message_id not in self.broadcasted_messages:
                self.broadcasted_messages.add(message_id)
                self.send_to_nodes(data, exclude=[node])
            
        # if self.callback is not None:
        #     self.callback("node_message", self, node, data)

    def outbound_node_connected(self, node):
        print("\033[94moutbound_node_connected: "  + node.host + ":" + str(node.port) + "\033[0m")

    def inbound_node_connected(self, node):
        print("\033[94minbound_node_connected: " + node.host + ":" + str(node.port) + "\033[0m")

    def inbound_node_disconnected(self, node):
        print("\033[94minbound_node_disconnected: "  + node.host + ":" + str(node.port) + "\033[0m")

    def outbound_node_disconnected(self, node):
        print("\033[94moutbound_node_disconnected: "  + node.host + ":" + str(node.port) + "\033[0m")

    def node_disconnect_with_outbound_node(self, node):
        print("\033[94mnode wants to disconnect with other outbound node: " + node.host + ":" + str(node.port) + "\033[0m")

    def node_request_to_stop(self):
        print("\033[94mnode is requested to stop: " + self.host + "\033[0m")
