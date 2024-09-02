from node_final import Node
from constants import *

class DsBase (Node):

    # Python class constructor
    def _init_(self, host, port, id=None , messageTosend = "" , callback=None, max_connections=5):
        super(DsBase, self)._init_(host, port, id, callback, max_connections)
        print("\033[92mBase: Started\033[0m")
        self.messageTosend = messageTosend
        
    def outbound_node_connected(self, node):
        print(f"\033[92moutbound_node_connected : {node.host}:{node.port} \033[0m")

    def inbound_node_connected(self, node):
        print(f"\033[92minbound_node_connected : {node.host}:{node.port} \033[0m")

    def inbound_node_disconnected(self, node):
        print(f"\033[92minbound_node_disconnected : {node.host}:{node.port} \033[0m")

    def outbound_node_disconnected(self, node):
        print(f"\033[92moutbound_node_disconnected : {node.host}:{node.port} \033[0m")
        
    def start_the_protocol(self):
        self.send_to_nodes(Message("Block #1", INFO , False, 1))