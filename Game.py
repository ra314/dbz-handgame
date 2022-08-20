import random
from Player import Player

class Game:
	def __init__(self, player1, player2):
		self._players = (player1, player2)
		self.curr_player = None
		self.next_player = None
		self.draw_buffer = []
		self._start()

	def draw(self):
		self.draw_buffer.append(
			f'{self._players[0].draw()} \n\n'
			f'{self._players[1].draw()} \n\n')

	def _start(self):
		self._add_game_reference_to_objects()
		self._select_first_player()

	def _add_game_reference_to_objects(self):
		for player in self._players:
			player.add_game_reference_to_objects(self)
			
	def _select_first_player(self):
		players = list(self._players)
		random.shuffle(players)
		self.curr_player, self.next_player = players
		self.draw_buffer.append(f'The first player is {self.curr_player}. \n')

	def request_move(self, player):
		# Getting and adding actions from the player
		player_actions_str, player_actions = player.get_actions()

		# Draw game and send available actions to server
		self.draw()
		return player_actions_str, player_actions

	def process_move(self, moves):
		for action_str, action in moves:
      if Player.is_evasive_action(action_str):
        action()
    for action_str, action in moves:
      if !is_evasive_action:
        action()

		# reset_evasion_state
		self.curr_player.reset_evasion_state()
		self.next_player.reset_evasion_state()
