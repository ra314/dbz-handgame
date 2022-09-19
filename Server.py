from Player import Player
from Game import Game
from copy import deepcopy


def enumerate_choices(choices):
	output = "Pick a number to select a choice\n"
	for index, choice in enumerate(choices):
		output += f"[{index}]: {choice}\n"
	return output


def create_player(client):
	client.send("Send name: ".encode())
	name = (client.recv(BUF_SIZE)).decode('utf-8')
	return Player(name)


def broadcast(client1, client2, message):
	message = message + separator
	client1.send(message.encode())
	client2.send(message.encode())


def receive_and_send_client_action(players_and_clients, game):
  actions_to_take = []
  for player, client in players_and_clients:
	  actions_str, actions = game.request_move(player)
	  assert(len(actions_str)>0)
	  assert(len(actions_str) == len(actions))
	  
	  message_to_client = str(
				          f"{game.draw_buffer.pop(0)} \n\n"
				          f"{enumerate_choices(actions_str)}{separator}")  
	  print(message_to_client)
	  
	  while True:
		  client.send(message_to_client.encode())
		  print("Waiting for response")
		  response = (client.recv(BUF_SIZE)).decode('utf-8')
		  if not response.isdigit():
		    print("An integer was not provided by the client.")
		    continue
		  num = int(response)
		  if num >= len(actions):
		    print("The selection action is out of bounds.")
		    continue
		  actions_to_take.append((actions_str[num], actions[num]))
		  break
  print(f"\"{actions_to_take}\" was selected as an action.")
  game.process_moves(actions_to_take)

def end_session(client):
	client.send("Session Over.\n".encode())


from PrepareSocket import *

# Connecting to clients
sock, TCP_IP = create_socket()
sock.bind((TCP_IP, T_PORT))
sock.listen()
client1, addr1 = sock.accept()
client2, addr2 = sock.accept()

# Getting player names
player1 = create_player(client1)
player2 = create_player(client2)
game = Game(player1, player2)
players_and_clients = [(player1, client1),(player2, client2)]

# Gameplay Loop
while True:
	while game.draw_buffer:
		broadcast(client1, client2, game.draw_buffer.pop(0))
	if receive_and_send_client_action(players_and_clients, game) == 0:
		break

# Ending connections with clients
end_session(client1)
end_session(client2)
