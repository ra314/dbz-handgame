from Player import Player
from Game import Game
from copy import deepcopy
import numpy as np
from PrepareSocket import *




class ClientWrapper:
  def __init__(self, connection):
    self.player = None
    pass
  def create_player(self):
    pass
  def send_message(self, message):
    pass
  def end_session(self):
    pass
  def select_action(self, game_state_str):
    pass
  def __str__(self):
    return str(self.player)

class AI_Client(ClientWrapper):
  AI_Client_count = 0
  
  def __init__(self, connection):
    self.player = None
    AI_Client.AI_Client_count += 1
    self.name = f'AI_{AI_Client.AI_Client_count}'
  def create_player(self):
    self.player = Player(self.name)
  def send_message(self, message):
    pass
  def end_session(self):
    pass
  def select_action(self, game_state_str):
    eqs, action_str, action = self.player.get_AI_action()
    action_str_and_probs = [f"{action_str}:{prob:.2f}" for prob, action_str in zip(eqs[0][0], self.player.get_actions()[0])]
    print(", ".join(action_str_and_probs))
    return action_str, action

class Networked_Client(ClientWrapper):
  def __init__(self, connection):
    self.connection = connection
    self.player = None
  def create_player(self):
    self.connection.send("Send name: ".encode())
    name = (self.connection.recv(BUF_SIZE)).decode('utf-8')
    self.player = Player(name)
  def send_message(self, message):
    self.connection.send(message.encode())
  def end_session(self):
	  self.connection.send("Session Over.\n".encode())
  def select_action(self, game_state_str):
    actions_str, actions = self.player.get_actions()
    assert(len(actions_str)>0)
    assert(len(actions_str) == len(actions))
    
    message_to_client = str(
		              f"{game_state_str} \n\n"
		              f"{enumerate_choices(actions_str)}{separator}")

    while True:
      self.connection.send(message_to_client.encode())
      print("Waiting for response")
      response = (self.connection.recv(BUF_SIZE)).decode('utf-8')
      if not response.isdigit():
        print("An integer was not provided by the client.")
        continue
      num = int(response)
      if num >= len(actions):
        print("The selection action is out of bounds.")
        continue
      return actions_str[num], actions[num]



def enumerate_choices(choices):
	output = "Pick a number to select a choice\n"
	for index, choice in enumerate(choices):
		output += f"[{index}]: {choice}\n"
	return output


# UNIT TESTING
# Testing Player.get_payout_table
want = [['Dodge', 'Block', 'Charge', 'Kamehameha'], [0,0,-1,1],[0,0,-1,-1],[1,1,0,-1],[-1,1,1,0]]
test_player1, test_player2 = Player(''), Player('')
test_player1.increase_charge()
test_player2.increase_charge()
got = Player.get_payout_table(test_player1, test_player2)
got.insert(0, test_player1.get_actions()[0])
assert(got == want)

# Testing AI reccomendation
test_game = Game(test_player1, test_player2)
assert(np.allclose(np.array(test_player1.get_AI_action()[0]), np.array([[0.33333333, 0.        , 0.33333333, 0.33333333], [0.33333333, 0.        , 0.33333333, 0.33333333]])))
test_player1.num_charges = 0
test_player2.num_charges = 0
assert(test_player1.get_AI_action()[1]=="Charge")

# Connecting to clients
sock, TCP_IP = create_socket()
sock.bind((TCP_IP, T_PORT))
sock.listen()

# Selecting number of AI players
print("This game is designed for 2 players.")
print("Enter the number of AI players you want in this game (0, 1 or 2): ")
while True:
  num_AI = input()
  if not num_AI.isdigit():
    print("An integer was not provided by the client.")
    continue
  num_AI = int(num_AI)
  if num_AI > 2 or num_AI < 0:
    print("Only 0, 1 and 2 are valid responses. Your selected resposne is invalid.")
    continue
  break

if num_AI == 2:
  client1 = AI_Client(None)
  client2 = AI_Client(None)
elif num_AI == 1:
  client1, client2 = AI_Client(None), Networked_Client(sock.accept()[0])
elif num_AI == 2:
  client1, client2 = Networked_Client(sock.accept()[0]), Networked_Client(sock.accept()[0])

# Getting player names
client1.create_player()
client2.create_player()
game = Game(client1.player, client2.player)

# Gameplay Loop
while True:
  print(game.draw())
  actions_to_take = [client1.select_action(game.draw()), client2.select_action(game.draw())]
  # print(f"\"{actions_to_take}\" was selected as an action.")
  game.process_moves(actions_to_take)
  if game.get_num_dead_players() > 0:
    break

# Ending connections with clients
print(game.draw())
client1.send_message(game.draw())
client2.send_message(game.draw())
print(game.get_end_screen())
client1.send_message(game.get_end_screen())
client2.send_message(game.get_end_screen())
client1.end_session()
client2.end_session()
