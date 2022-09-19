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
    HP_PER_SYMBOL = 10
    HP_str = ('+' * int(self.curr_HP/HP_PER_SYMBOL)) + ('-' * int((self.max_HP - self.curr_HP)/HP_PER_SYMBOL))
    return f"{self._name} \n" \
           f"HP: {HP_str} \n" \
           f"Charges: {self.num_charges} \n" \

  def attack(self, attack, defender):
    self.num_charges = max(0, self.num_charges-attack.num_charges_needed)
    print(attack)
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

  def change_HP(self, delta):
	  self.curr_HP += delta
	  self._game.draw()

  def add_game_reference_to_objects(self, game):
	  self._game = game

  def reset_evasion_state(self):
    self.curr_evasion_method = 0

  def increase_charge(self):
    self.num_charges += 1

  def set_evasion_method(self, evasion_method):
    self.curr_evasion_method = evasion_method
  
  non_offensive_actions = set(["Dodge", "Block", "Charge"])
  def is_non_offensive_action(action_str):
    return action_str in Player.non_offensive_actions

