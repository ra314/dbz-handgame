from Attack import attacks
import Evasion

class Player:
  max_HP = 100

  def __init__(self, name):
	  self._name = name
	  self.curr_HP = Player.max_HP
	  self._game = None
	  self.num_charges = 0
	  self.curr_evasion_method = 0

  def __str__(self):
	  return self._name

  def draw(self):
    HP_str = ('+' * int(self.curr_HP/5)) + ('-' * int((self.max_HP - self.curr_HP)/5))
    return f"{self._name} \n" \
           f"HP: {HP_str} \n"

  def attack(self, attack, defender):
    self.num_charges -= attack.num_charges_needed
    if defender.curr_evasion_method != attack.evasion_method:
      defender.change_HP(-attack.power)

  def get_available_attacks(self):
    attack_actions_str, attack_actions = [], []
    for attack in attacks:
      if attack.num_charges_needed <= self.num_charges:
        attack_actions_str.append(attack.name)
        attack_actions.append(lambda: self.attack(attack, self._game.next_player))
    return attack_actions_str, attack_actions

  def get_actions(self):
	  actions_str = ["Dodge", "Block", "Charge"]
	  actions = [lambda: self.set_evasion_method(Evasion.DODGE), \
	            lambda: self.set_evasion_method(Evasion.BLOCK), \
	            lambda: self.increase_charge()]
	  # Add attacks if the player has enough charges for it
	  attack_actions_str, attack_actions = self.get_available_attacks()
	  actions_str.extend(attack_actions_str)
	  actions.extend(attack_actions)
	  return actions_str, actions

  def change_HP(self, delta):
	  # Clamping HP
	  # The max of current and max hp is done in the case of the start where p2 has 5 extra HP
	  self.curr_HP = min(max(0, delta+self.curr_HP), max(self.curr_HP, Player.max_HP))
	  self._game.draw()

  def add_game_reference_to_objects(self, game):
	  self._game = game

  def reset_evasion_state(self):
    self.curr_evasion_method = 0

  def increase_charge(self):
    self.num_charges += 1

  def set_evasion_method(self, evasion_method):
    self.evasion_method = evasion_method
  
  evasion_actions = set(["Dodge", "Block"])
  def is_evasive_action(action_str):
    return action_str in evasion_actions

