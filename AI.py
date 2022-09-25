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
  
  @abstractmethod
  def name(self):
    return "Abstract Class"
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

# The evaluators ASSUME num_charges_needed * 10 = power of an attack.

# Does not consider previous actions.
# Does not consider the consequence of losing charges when hit by an attack.
# When hit by an attack, the eval is the same as the power of that attack.
class Evaluator_1(Evaluator):
  def name(self):
    return "OG"
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

# Does not consider previous actions.
# Considers consequence of losing charges when hit by an attack.
# When hit by an attack, the damage it carries does not matter, only the number of charges lost.
# It considers 1 held charge to be just as good as 1 damage dealth.
# Because of this when an attack is landed the only matter of significance is how many charges
# the opponent lost as a consequence.
class Evaluator_2(Evaluator):
  def name(self):
    return "v2"
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

# Does not consider previous actions.
# epsilon = value(1 damage)/value(1 charge)
# The higher epsilon is, the more emphasis is placed on landing a hit.
class Evaluator_3(Evaluator):
  # calc_value_of_attack
  def cvoa(self, charges_spent):
    EPSILON = 2
    return - charges_spent + (charges_spent*EPSILON)
  def name(self):
    return "v3"
  def player_hasher(self, player):
    return player.num_charges
  def charge_evade(self, action1_str, action2_str, player1, player2):
    return +1
  def charge_charge(self, action1_str, action2_str, player1, player2):
    return 0
  def charge_attack(self, action1_str, action2_str, player1, player2):
    return -self.cvoa(indexed_attacks[action2_str].num_charges_needed)
  def evade_evade(self, action1_str, action2_str, player1, player2):
    return 0
  def evade_attack_miss(self, action1_str, action2_str, player1, player2):
    return +indexed_attacks[action2_str].num_charges_needed
  def evade_attack_hit(self, action1_str, action2_str, player1, player2):
    return -player1.num_charges-self.cvoa(indexed_attacks[action2_str].num_charges_needed)
  def attack_attack(self, action1_str, action2_str, player1, player2):
    player1_remaining_charges = player1.num_charges - indexed_attacks[action1_str].num_charges_needed
    player2_remaining_charges = player2.num_charges - indexed_attacks[action2_str].num_charges_needed
    spent_charges1 = indexed_attacks[action1_str].num_charges_needed
    spent_charges2 = indexed_attacks[action2_str].num_charges_needed
    return -player1_remaining_charges+player2_remaining_charges+self.cvoa(spent_charges1)-self.cvoa(spent_charges2)

evaluators = [Evaluator_1(), Evaluator_2(), Evaluator_3()]
