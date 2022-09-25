import random
from Player import Player

class Game:
  def __init__(self, player1, player2):
	  self._players = (player1, player2)
	  self.draw_buffer = []
	  self._start()
	  self.num_turns = 0

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
    
    self.num_turns += 1
  
  def get_other_player(self, player):
    index = self._players.index(player)
    return self._players[1-index] 
  
  def get_num_dead_players(self):
    return sum([player.is_dead() for player in self._players])
  
  def get_loser(self):
    dead_people = list(filter(lambda x: x.is_dead(), self._players))
    if len(dead_people) == 1:
      return dead_people[0]
    return None
  
  def get_end_screen(self):
    num_dead_players = self.get_num_dead_players()
    if num_dead_players == 0:
      return ""
    elif num_dead_players == 2:
      return f"Both{self._players[0]._name} and {self._players[1]._name} died\n"
    elif num_dead_players == 1:
      loser = self.get_loser()
      winner = self.get_other_player(loser)
      return f"{winner} won and {loser} lost"
    return ""
