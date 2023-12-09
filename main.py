from game import Game
import sys

# NOTE: honestly we COULD make another caretaker class called "GameManager" and use it as a composition object
# in the CLI. This leads to better generalization into the GUI interface, instead of using the CLI as the caretaker.
# But if we limit the scope to this assignment (for the purpose of exercising), the difference is minimal.

class GameCLI:
  """
    The "Caretaker" of the Memento Design Pattern.
    The Caretaker doesn't depend on the Concrete Memento GameSave. Therefore, it
    doesn't have access to the originator's (Game's) state, stored inside the memento GameSave. It
    works with all mementos via the base Memento interface.
  """

  def __init__(self):  # Have the game initialize the originator during run based on CLI args
    self._game_saves = []  # ._mementos

  # def _backup(self):
  #   # NOTE: should've been public in a caretaker interface. But since we are merging it with CLI
  #   # and only using it in CLI, it can be private.
  #   self._game_saves.append(self._game.save())

  def _push_pop_switch(self, push_list, pop_list):
    # Likely so
    '''An _undo ADAPTED to perform both undo or redo functionality'''
    if not len(pop_list):
      return  # nothing to restore to

    push_list.append(self._game.save())  # Save the current state into push list
    game_save = pop_list.pop()  # a memento
    self._game.restore(game_save)
    # try:  # no concern regarding failed restoration check for now.
    #     self._originator.restore(memento)
    # except Exception:
    #     self.undo()

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
      self._game = Game(player1, player2)  # should trigger the __new__ to overwrite the old game
      redo_saves = []

      # Let CLI manage the game session. (Alternative: let Game manage it, and use try-except to break out)
      while True: # while game is not over, players move
        # pre-choice print statements:
        print(self._game)
        # If the undo_redo option is enabled.
        if undo_redo:
          choice = input("undo, redo, or next\n")
          # NOTE: my interpretation based on the example: the list for UNDO is ongoing. But REDO's list only exists within
          # this current scope of undo_redo. Once NEXT is called, REDO is resetted.
          # Also this isn't in the example, but I assume we can undo into a redo into undo.
          if choice == "undo":
            self._push_pop_switch(redo_saves, self._game_saves)
            continue
          elif choice == "redo":
            self._push_pop_switch(self._game_saves, redo_saves)
            continue
          elif choice == "next":
            self._game_saves.append(self._game.save())  # save the previous state
            redo_saves = []
          else:
            pass # input error check for this?

        # Play one step of the game.
        winner = self._game.run_one_step()
        if winner:  # game has ended!
          print("{} has won".format(winner))
          break
        else:  # game is on going. Use this window to ask.
          # TODO: add post-choice print statements here.
          pass

      want_to_play = input("Play again?\n")



if __name__=='__main__':
  GameCLI().run()
  # test = Game("human", "heuristic", None, None)
  # # test2 = Game(True, True, False, False)
  # # print(test2)
  # print(test)
  # test._players[0]._workers['A'].move('n')
  # print(test)
