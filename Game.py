import random
from Player import Player

class Game:
  def __init__(self, player1, player2):
	  self._players = (player1, player2)
	  self.draw_buffer = []
	  self._start()

  def draw(self):
	  return (
		  f'{self._players[0].draw()} \n\n'
		  f'{self._players[1].draw()} \n\n')

  def _start(self):
	  self._add_game_reference_to_objects()

  def _add_game_reference_to_objects(self):
	  for player in self._players:
		  player.add_game_reference_to_objects(self)

  def process_moves(self, moves):
    # Make the evasive actions go before the attacking actions
    for action_str, action in moves:
      if action_str in Player.non_offensive_actions:
        action()
    for action_str, action in moves:
      if action_str not in Player.non_offensive_actions:
        action()

    # reset_evasion_state
    for player in self._players:
      player.reset_evasion_state()
  
  def get_other_player(self, player):
    index = self._players.index(player)
    return self._players[1-index] 
