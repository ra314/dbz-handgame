import random
from Player import Player

class Game:
  def __init__(self, player1, player2):
	  self._players = (player1, player2)
	  self.draw_buffer = []
	  self._start()

  def draw(self):
	  self.draw_buffer.append(
		  f'{self._players[0].draw()} \n\n'
		  f'{self._players[1].draw()} \n\n')

  def _start(self):
	  self._add_game_reference_to_objects()
	  self.draw_buffer.append(f'Game starting now. \n')

  def _add_game_reference_to_objects(self):
	  for player in self._players:
		  player.add_game_reference_to_objects(self)
	
  def request_move(self, player):
	  # Getting and adding actions from the player
	  player_actions_str, player_actions = player.get_actions()

	  # Draw game and send available actions to server
	  self.draw()
	  return player_actions_str, player_actions

  def process_moves(self, moves):
    # Make the evasive actions go before the attacking actions
    for action_str, action in moves:
      if Player.is_evasive_action(action_str):
        action()
    for action_str, action in moves:
      if not Player.is_evasive_action(action_str):
        action()

    # reset_evasion_state
    for player in self._players:
      player.reset_evasion_state()
