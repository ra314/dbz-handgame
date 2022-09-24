import os
from PrepareSocket import *
from multiprocessing import Process, Queue
import sys

# Responding to the server
def respond(sock):
	# Sending back a message, if the input isn't empty
	while True:
	  message = input()
	  if message:
		  sock.send(message.encode())
		  break

def read_from_network(data_queue, sock):
  while True:
    # Parsing server info
    data = sock.recv(BUF_SIZE).decode('utf-8')
    # Parsing data buffer
    for data_chunk in data.split(separator):
      data_queue.put(data_chunk)

def process_data_queue(data_queue, sock):
  while True:
    # Retrieving latest part of buffer
    data = data_queue.get()
    if data == "":
      continue
	  # Clearing previous print
    os.system('cls' if os.name == 'nt' else 'clear')
    print(data, end="")

	  # Ending session
    if data == "Session Over.\n":
      return 0
		  
    respond(sock)

if __name__ == "__main__":
  data_queue = Queue()
  # Connecting to server
  sock, TCP_IP = create_socket()
  sock.connect((TCP_IP, T_PORT))
  # Data retrival loop
  retrival_process = Process(target=read_from_network, args=(data_queue,sock,), name="retriever")
  retrival_process.start()
  # Data processing loop
  process_data_queue(data_queue, sock)
