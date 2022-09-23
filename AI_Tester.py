from Player import Player
from AI import eval_funcs
from Server import AI_Client
from Game import Game

def pretty_print(matrix):
  s = [[str(e) for e in row] for row in matrix]
  lens = [max(map(len, col)) for col in zip(*s)]
  fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
  table = [fmt.format(*row) for row in s]
  return '\n'.join(table)

result_table = []
for eval_func_1 in eval_funcs:
  for eval_func_2 in eval_funcs:
    wins, draws, losses = 0, 0, 0
    for i in range(100):
      client1, client2 = AI_Client(None, eval_func_1), AI_Client(None, eval_func_2)
      client1.create_player()
      client2.create_player()
      game = Game(client1.player, client2.player)
      while True:
        actions_to_take = [client1.select_action(None), client2.select_action(None)]
        game.process_moves(actions_to_take)
        if game.get_num_dead_players() > 0:
          break
      num_dead_people = game.get_num_dead_players()
      if num_dead_people == 2:
        ties +=1
      elif num_dead_people == 1:
        if game.get_loser() == client1.player:
          wins += 1
        else:
          losses += 1
      else:
        assert(False)
      print((wins, draws, losses))
    result_table.append((wins, draws, losses))

print(pretty_print(result_table))
