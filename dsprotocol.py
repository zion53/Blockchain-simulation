import sys
import time
import socket
sys.path.insert(0, '..') # Import the files where the modules are located

from DsBase import DsBase
from Miner import Miner
from Full_node import FullNode
from Light_node import LightNode
from constants import *

def get_ip_address():
    try:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Connect to a remote server (doesn't have to be reachable)
        s.connect(("8.8.8.8", 80))
        # Get the local IP address
        ipv4_address = s.getsockname()[0]
        return ipv4_address
    except Exception as e:
        print("Error occurred while getting IPv4 address:", e)
        return None

ip = get_ip_address()
print("\033[92m" + f"Your ip is {ip}\n" + "\033[0m")
node_1 = DsBase(ip, 8001)
node_1.start()
print("\033[92m\nPress 1 to start the protocol\033[0m")
choice = int(input())
if choice == 1:
    node_1.start_the_protocol()