from Player import Player
from Attack import indexed_attacks
from Evasion import Evasion

class Evaluator:
  def __init__(self, eval_func, player_hasher):
    self.eval_func = eval_func
    # This is used to avoid repeatedly calculating the payout table if the relevant conditions
    # (in this case the state of the player) is the same.
    self.player_hasher = player_hasher

# Methods in this file returns the evaluation of a given action pair.
# Eval is positive if the person performing action1 ends up better off
# Game is assumed to be zero sum

def eval_1(action1_str, action2_str, player1, player2):
  if action1_str == "Charge":
    if action2_str in Player.evasive_actions:
      return +1
    elif action2_str == "Charge":
      return 0
    elif action2_str in indexed_attacks:
      return -indexed_attacks[action2_str].power//10
    else:
      assert(False)
  elif action1_str in Player.evasive_actions:
    if action2_str in Player.evasive_actions:
      return 0
    elif action2_str in indexed_attacks:
      performed_evasion_method = Evasion[action1_str.upper()].value
      required_evasion_method = indexed_attacks[action2_str].evasion_method.value
      multiplier = 1 if performed_evasion_method == required_evasion_method else -1
      return indexed_attacks[action2_str].power//10 * multiplier
    else:
      return -eval_1(action2_str, action1_str, player2, player1)
  elif action1_str in indexed_attacks:
    if action2_str in indexed_attacks:
      return (indexed_attacks[action1_str].power - indexed_attacks[action2_str].power)//10
    else:
      return -eval_1(action2_str, action1_str, player2, player1)
  # Only the top right diagonal of possible action interactions are coded up
  # Since it doesn't matter who played it and we assume the game is zero sum
  else:
    assert(False)

evaluators = [Evaluator(eval_1, lambda x: x.num_charges)]
