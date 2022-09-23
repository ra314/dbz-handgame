from Attack import attacks, indexed_attacks
from Evasion import Evasion
import nashpy as nash
import numpy as np

class Player:
  max_HP = 100

  def __init__(self, name, evaluator):
	  self._name = name
	  self.curr_HP = Player.max_HP
	  self._game = None
	  self.num_charges = 0
	  self.curr_evasion_method = 0
	  self.prev_action = ""
	  self.evaluator = evaluator

  def __str__(self):
	  return self._name

  def draw(self):
    HP_PER_SYMBOL = 10
    HP_str = ('+' * int(self.curr_HP/HP_PER_SYMBOL)) + ('-' * int((self.max_HP - self.curr_HP)/HP_PER_SYMBOL))
    return f"{self._name} \n" \
           f"HP: {HP_str} \n" \
           f"Charges: {self.num_charges} \n" \
           f"Previous action: {self.prev_action} \n" \

  def attack(self, attack, defender):
    self.prev_action = f"Performed {attack.name}"
    self.num_charges = max(0, self.num_charges-attack.num_charges_needed)
    if defender.curr_evasion_method != attack.evasion_method:
      defender.change_HP(-attack.power)
      # Take away charges if you get hit
      defender.num_charges = 0

  def get_available_attacks(self):
    attack_actions_str, attack_actions = [], []
    for attack in attacks:
      if self.num_charges >= attack.num_charges_needed:
        attack_actions_str.append(attack.name)
        attack_actions.append(lambda attack=attack: self.attack(attack, self._game.get_other_player(self)))
    return attack_actions_str, attack_actions

  def get_actions(self):
	  actions_str = list(Player.non_offensive_actions)
	  actions = [lambda: self.set_evasion_method(Evasion.DODGE), \
	            lambda: self.set_evasion_method(Evasion.BLOCK), \
	            lambda: self.increase_charge()]
	  # Add attacks if the player has enough charges for it
	  attack_actions_str, attack_actions = self.get_available_attacks()
	  actions_str.extend(attack_actions_str)
	  actions.extend(attack_actions)
	  return actions_str, actions
	
  # Returns the action that the AI would do, if it were the player
  # This is non deterministic since we'll be using Mixed Strategy Nash Equilbria
  nash_games = {}
  def get_AI_action(self):
    player1, player2 = self, self._game.get_other_player(self)
    key = (self.evaluator.player_hasher(player1), self.evaluator.player_hasher(player2))
    if key in Player.nash_games:
      eqs = Player.nash_games[key]
    else:
      payoff_table = Player.get_payout_table(self, player2, self.evaluator)
      dbz = nash.Game(payoff_table)
      eqs = list(dbz.support_enumeration())
      Player.nash_games[key] = eqs
    actions_str, actions = self.get_actions()
    selected_index = np.random.choice(len(actions_str), 1, p=eqs[0][0])[0]
    return eqs, actions_str[selected_index], actions[selected_index]
  
  # This should be updated to 
  def get_ai_hashkey(self):
    return self.num_charges
  
  def get_payout_table(player1, player2, evaluator):
    table = []
    for action1_str in player1.get_actions()[0]:
      table.append([])
      for action2_str in player2.get_actions()[0]:
        payoff = evaluator.eval(action1_str, action2_str, player1, player2)
        table[-1].append(payoff)
    return np.array(table)
  
  def change_HP(self, delta):
	  self.curr_HP = max(self.curr_HP+delta, 0)
	
  def is_dead(self):
    return self.curr_HP == 0

  def add_game_reference_to_objects(self, game):
	  self._game = game

  def reset_evasion_state(self):
    self.curr_evasion_method = 0

  def increase_charge(self):
    self.prev_action = "Tried to charge"
    self.num_charges += 1

  def set_evasion_method(self, evasion_method):
    self.prev_action = f"Tried to {str(Evasion(evasion_method)).replace('Evasion.', '').lower()}"
    self.curr_evasion_method = evasion_method
  
  non_offensive_actions = ("Dodge", "Block", "Charge")
  evasive_actions = ("Dodge", "Block")
