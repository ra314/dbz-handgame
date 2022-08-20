import socket
T_PORT = 12345
TCP_IP = '127.0.0.1'
BUF_SIZE = 4096

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Selecting IP address
selected_TCP_IP = input("Type in the server's IP address. Leave blank to use local host.\n")
if selected_TCP_IP:
	TCP_IP = selected_TCP_IP

#Ensuring the socket is closed
import atexit
def close_socket():
	print("Socket closed.")
	sock.close()

atexit.register(close_socket)

separator = "ENDENDEND"
