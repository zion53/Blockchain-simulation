from node_final import Node
from constants import *
import hashlib
import threading

class DSNode (Node):

    # Python class constructor
    def __init__(self, host, port, n, delta, id=None, callback=None, max_connections=5):
        super(DSNode, self).__init__(host, port, id, callback, max_connections)
        self.pool = set()
        self.rounds = 2
        self.round_time = delta
        self.start_time = -1
        print("\033[93mDS Node: Started\033[0m")


    def node_message(self, node, data):
        """This method is invoked when a node send us a message.
            data is a string, need to convert to a message object
        """
        parts = str(data).split(":")
        messagebody = parts[0]
        type = int(parts[1])
        isBroadcast = parts[2]
        message_id = parts[3]
        num = int(parts[4])
        i = 1
        num_sign = bin(num).count('1')
        if (num & (1<<i)) == 0:
            num |= (1<<i)
        
        if self.start_time == -1:
            self.start_time = int(time.time())
            def start_give_results():
                t = threading.Thread(target=self.give_results)
                t.daemon = True
                t.start()
            start_give_results()
        round_num =int( (int(time.time()) - self.start_time)/(self.round_time))
        if num_sign == round_num+1:
            self.pool.add(messagebody)
            self.send_to_nodes(Message(messagebody, type, isBroadcast, num), exclude=[node])
        
    def give_results(self):
        time.sleep((self.rounds)*(self.round_time))
        if len(self.pool) == 1:
            print("Message accepted: " + next(iter(self.pool)))
        else :
            print("no message")
        
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
