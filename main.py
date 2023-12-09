from game import Game
import sys

class GameCLI:
  """
    The "Caretaker" of the Memento Design Pattern.
    The Caretaker doesn't depend on the Concrete Memento GameSave. Therefore, it
    doesn't have access to the originator's (Game's) state, stored inside the memento GameSave. It
    works with all mementos via the base Memento interface.
  """

  def __init__(self):  # Have the game initialize the originator during run based on CLI args
    self._game_saves = []  # ._mementos

  def run(self):
    '''Starts the CLI application'''
    # library of values
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
    
    # start the game cycle.
    want_to_play = "yes"
    while want_to_play == "yes":
      # the Originator set-up
      self._game = Game(player1, player2, undo_redo, enable_score)  # should trigger the __new__ to overwrite the old game

      # Let CLI manage the game session. (Alternative: let Game manage it, and use try-except to break out)
      while True: # while game is not over, players move
        # pre-choice print statements
        print(self._game)

        winner = self._game.run_one_round()
        if winner:  # game has ended!
          print("{} has won".format(winner))
          break
        else:  # game is on going. Use this window to ask.
          # TODO: add post-choice print statements here.
          pass

      want_to_play = input("Play again?")



if __name__=='__main__':
  GameCLI().run()
  # test = Game("human", "heuristic", None, None)
  # # test2 = Game(True, True, False, False)
  # # print(test2)
  # print(test)
  # test._players[0]._workers['A'].move('n')
  # print(test)
