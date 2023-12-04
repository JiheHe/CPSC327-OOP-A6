from game import Game
import sys

class GameCLI:
  def run(self):
    player_type = ["human", "heuristic", "random"]
    commands = ["on", "off"]
    args = sys.argv[1:]
    # Set default values
    player1, player2, undo_redo, enable_score = "human", "human", "off", "off"
    
    # if specified in command line, replace default values
    if len(args) >= 1:
      player1 = args[0]
    if len(args) >= 2:
      player2 = args[1]
    if len(args) >= 3:
      undo_redo = args[2]
    if len(args) >= 4:
      enable_score = args[3]
    
    # check if command line args are valid:
    if player1 not in player_type or player2 not in player_type or undo_redo not in commands or enable_score not in commands:
      print("Command line error")
      return 1
    
    want_to_play = "yes"
    while want_to_play == "yes":
      test = Game(player1, player2, undo_redo, enable_score)
      test.run()
      want_to_play = input("Play again?")



if __name__=='__main__':
  test = Game("human", "heuristic", None, None)
  # test2 = Game(True, True, False, False)
  # print(test2)
  print(test)
  test._players[0]._workers['A'].move('n')
  print(test)
