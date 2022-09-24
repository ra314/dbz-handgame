from Player import Player
from Attack import indexed_attacks
from Evasion import Evasion
from abc import ABC, abstractmethod

class Evaluator(ABC):
  # Returns the evaluation of a given action pair.
  # Eval is positive if the person performing action1 ends up better off
  # Game is assumed to be zero sum
  def eval(self, action1_str, action2_str, player1, player2):
    if action1_str == "Charge":
      if action2_str in Player.evasive_actions:
        return self.charge_evade(action1_str, action2_str, player1, player2)
      elif action2_str == "Charge":
        return self.charge_charge(action1_str, action2_str, player1, player2)
      elif action2_str in indexed_attacks:
        return self.charge_attack(action1_str, action2_str, player1, player2)
      else:
        assert(False)
    elif action1_str in Player.evasive_actions:
      if action2_str in Player.evasive_actions:
        return self.evade_evade(action1_str, action2_str, player1, player2)
      elif action2_str in indexed_attacks:
        performed_evasion_method = Evasion[action1_str.upper()].value
        required_evasion_method = indexed_attacks[action2_str].evasion_method.value
        if performed_evasion_method == required_evasion_method:
          return self.evade_attack_miss(action1_str, action2_str, player1, player2)
        else:
          return self.evade_attack_hit(action1_str, action2_str, player1, player2)
      else:
        return -self.eval(action2_str, action1_str, player2, player1)
    elif action1_str in indexed_attacks:
      if action2_str in indexed_attacks:
        return self.attack_attack(action1_str, action2_str, player1, player2)
      else:
        return -self.eval(action2_str, action1_str, player2, player1)
    # Only the top right diagonal of possible action interactions are coded up
    # Since it doesn't matter who played it and we assume the game is zero sum
    else:
      assert(False)
    
  # This is used to avoid repeatedly calculating the payout table if the relevant conditions
  # (in this case the state of the player) is the same.
  @abstractmethod
  def player_hasher(self, player):
    pass
  @abstractmethod
  def charge_evade(self, action1_str, action2_str, player1, player2):
    pass
  @abstractmethod
  def charge_charge(self, action1_str, action2_str, player1, player2):
    pass
  @abstractmethod
  def charge_attack(self, action1_str, action2_str, player1, player2):
    pass
  @abstractmethod
  def evade_evade(self, action1_str, action2_str, player1, player2):
    pass
  @abstractmethod
  def evade_attack_miss(self, action1_str, action2_str, player1, player2):
    pass
  @abstractmethod
  def evade_attack_hit(self, action1_str, action2_str, player1, player2):
    pass
  @abstractmethod
  def attack_attack(self, action1_str, action2_str, player1, player2):
    pass

class Evaluator_1(Evaluator):
  def player_hasher(self, player):
    return player.num_charges
  def charge_evade(self, action1_str, action2_str, player1, player2):
    return +1
  def charge_charge(self, action1_str, action2_str, player1, player2):
    return 0
  def charge_attack(self, action1_str, action2_str, player1, player2):
    return -indexed_attacks[action2_str].power//10
  def evade_evade(self, action1_str, action2_str, player1, player2):
    return 0
  def evade_attack_miss(self, action1_str, action2_str, player1, player2):
    return +indexed_attacks[action2_str].power//10
  def evade_attack_hit(self, action1_str, action2_str, player1, player2):
    return -indexed_attacks[action2_str].power//10
  def attack_attack(self, action1_str, action2_str, player1, player2):
    return (indexed_attacks[action1_str].power - indexed_attacks[action2_str].power)//10

# With this
class Evaluator_2(Evaluator):
  def player_hasher(self, player):
    return player.num_charges
  def charge_evade(self, action1_str, action2_str, player1, player2):
    return +1
  def charge_charge(self, action1_str, action2_str, player1, player2):
    return 0
  def charge_attack(self, action1_str, action2_str, player1, player2):
    return -player1.num_charges
  def evade_evade(self, action1_str, action2_str, player1, player2):
    return 0
  def evade_attack_miss(self, action1_str, action2_str, player1, player2):
    return +indexed_attacks[action2_str].num_charges_needed
  def evade_attack_hit(self, action1_str, action2_str, player1, player2):
    return -player1.num_charges
  def attack_attack(self, action1_str, action2_str, player1, player2):
    player1_remaining_charges = player1.num_charges - indexed_attacks[action1_str].num_charges_needed
    player2_remaining_charges = player2.num_charges - indexed_attacks[action2_str].num_charges_needed
    return -player1_remaining_charges+player2_remaining_charges

evaluators = [Evaluator_1(), Evaluator_2()]
