from Attack import attacks, indexed_attacks
from Evasion import Evasion
import nashpy as nash
import numpy as np

class Player:
  max_HP = 100

  def __init__(self, name):
	  self._name = name
	  self.curr_HP = Player.max_HP
	  self._game = None
	  self.num_charges = 0
	  self.curr_evasion_method = 0
	  self.prev_action = ""

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
  def get_AI_action(self):
    payoff_table = np.array(Player.get_payout_table(self, self._game.get_other_player(self)))
    dbz = nash.Game(payoff_table)
    eqs = list(dbz.support_enumeration())
    actions_str, actions = self.get_actions()
    selected_index = np.random.choice(len(actions_str), 1, p=eqs[0][0])[0]
    return eqs, actions_str[selected_index], actions[selected_index]
	  
  # Returns the evaluation of a given action pair.
  # Eval is positive if the person performing action1 ends up better off
  # For example if the actions are dodge and dodge, the eval is 0
  # If the actions are charge and kamehameha, the eval is -1
  def evaluate_action_pair(action1_str, action2_str):
    if action1_str == "Charge":
      if action2_str in Player.evasive_actions:
        return +1
      elif action2_str == "Charge":
        return 0
      elif action2_str in indexed_attacks:
        return -indexed_attacks[action2_str].power//10
      else:
        return -Player.evaluate_action_pair(action2_str, action1_str)
    elif action1_str in Player.evasive_actions:
      if action2_str in Player.evasive_actions:
        return 0
      elif action2_str in indexed_attacks:
        performed_evasion_method = Evasion[action1_str.upper()].value
        required_evasion_method = indexed_attacks[action2_str].evasion_method.value
        multiplier = 1 if performed_evasion_method == required_evasion_method else -1
        return indexed_attacks[action2_str].power//10 * multiplier
      else:
        return -Player.evaluate_action_pair(action2_str, action1_str)
    elif action1_str in indexed_attacks:
      if action2_str in indexed_attacks:
        return (indexed_attacks[action1_str].power - indexed_attacks[action2_str].power)//10
      else:
        return -Player.evaluate_action_pair(action2_str, action1_str)
    # Only the top right diagonal of possible action interactions are coded up
    # Since it doesn't matter who played it and we assume the game is zero sum
    # If the action_str is invalid, this will result in stackoverflow
    else:
      return -evaluate_action_pair(action2_str, action1_str)
  
  def get_payout_table(player1, player2):
    table = []
    for action1_str in player1.get_actions()[0]:
      table.append([])
      for action2_str in player2.get_actions()[0]:
        payoff = Player.evaluate_action_pair(action1_str, action2_str)
        #table[-1].append((payoff, action1_str, action2_str))
        table[-1].append(payoff)
    return table
  
  def change_HP(self, delta):
	  self.curr_HP += delta

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
