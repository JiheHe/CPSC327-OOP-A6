from game import Game
import sys
from abc import ABC, abstractmethod

# --------------------------------------DECORATOR SETUP PORTION START----------------------------------------------#

class CLI(ABC):  # Component
  """
  Define the interface for objects that can have responsibilities
  added to them dynamically.
  """

  @abstractmethod
  def pregame_statements(self):
    '''The statements to print / query for before each round of game in the CLI'''
    pass

  @abstractmethod
  def reset_game(self):
    '''reset the gameboard'''
    pass

  @abstractmethod
  def run(self):
    '''run the cli'''
    pass

class Decorator(CLI, ABC):
  """
  Maintain a reference to a Component object and define an interface
  that conforms to Component's interface.
  """

  def __init__(self, cli):
    self._cli = cli

  @abstractmethod
  def pregame_statements(self):
    self._cli.pregame_statements()

  @abstractmethod
  def reset_game(self):
    self._cli.reset_game()

  @abstractmethod
  def run(self):
    pass

class SaveDecorator(Decorator):
  """
  Add responsibilities to the component.
  """

  # NOTE: I think it's appropriate to reach into _cli for _game because this is a decorator class
  # so it's technically operating within the conceptual bound of GameCLI, which has a direct
  # access to _game.

  def _push_pop_switch(self, push_list, pop_list):
    # Likely so
    '''An _undo ADAPTED to perform both undo or redo functionality'''
    if not len(pop_list):
      return  # nothing to restore to

    push_list.append(self._cli._game.save())  # Save the current state into push list
    game_save = pop_list.pop()  # a memento
    self._cli._game.restore(game_save)
    # try:  # no concern regarding failed restoration check for now.
    #     self._originator.restore(memento)
    # except Exception:
    #     self.undo()

  def pregame_statements(self):
    '''Includes undo/redo query functionality'''
    super().pregame_statements()

    choice = input("undo, redo, or next\n")
    # NOTE: my interpretation based on the example: the list for UNDO is ongoing. But REDO's list only exists within
    # this current scope of undo_redo. Once NEXT is called, REDO is resetted.
    # Also this isn't in the example, but I assume we can undo into a redo into undo.
    if choice == "undo":
      self._push_pop_switch(self._redo_saves, self._game_saves)
      return True  # indicates continue
    elif choice == "redo":
      self._push_pop_switch(self._game_saves, self._redo_saves)
      return True
    elif choice == "next":  # indicates continue
      self._game_saves.append(self._cli._game.save())  # save the previous state
      self._redo_saves = []
    else:
      pass # input error check for this?
  
  def reset_game(self):
    '''Includes undo/redo state functionality'''
    super().reset_game()

    self._game_saves = []  # ._mementos
    self._redo_saves = []

  def run(self):
    '''Starts the CLI application with modified undo/redo parts'''
    # NOTE: the issue is that due to Python's dynamic logic, when I call the internal logic of run in the concrete
    # class, it is using the base implementation of them not knowing that they've been wrapped. So I either have
    # to duplicate code or slightly break the principle. Since we only have 1 decorator here, I think it's okay
    # to set up as below using some command concept of first order function.
    self._cli.run(self.pregame_statements, self.reset_game)

# --------------------------------------DECORATOR SETUP PORTION END----------------------------------------------#

# NOTE: honestly we COULD make another caretaker class called "GameManager" and use it as a composition object
# in the CLI. This leads to better generalization into the GUI interface, instead of using the CLI as the caretaker.
# But if we limit the scope to this assignment (for the purpose of exercising), the difference is minimal.

class GameCLI(CLI):
  """
    The "Caretaker" of the Memento Design Pattern. The "ConcreteComponent" of the Decorator design pattern.
    # NOTE: the Memento's caretaker portion is offloaded to the Decorator enhancement portion.
    The Caretaker doesn't depend on the Concrete Memento GameSave. Therefore, it
    doesn't have access to the originator's (Game's) state, stored inside the memento GameSave. It
    works with all mementos via the base Memento interface.
  """

  def __init__(self, player1, player2, enable_score):  # Have the game initialize the originator during run based on CLI args
    self._player1 = player1
    self._player2 = player2
    self._enable_score = enable_score

  def reset_game(self):
    '''Reset the gameboard'''
    self._game = Game(self._player1, self._player2, self._enable_score)  # should trigger the __new__ to overwrite the old game

  def pregame_statements(self):
    '''Print the current boardstate and gamestate'''
    print(self._game)

  def run(self, pregame_func=None, reset_func=None):  # using first-order injection.
    '''Starts the CLI application'''
    
    # start the game cycle.
    want_to_play = "yes"
    while want_to_play == "yes":
      # the Originator set-up
      (reset_func() if reset_func else self.reset_game())

      # Let CLI manage the game session. (Alternative: let Game manage it, and use try-except to break out)
      while True: # while game is not over, players move
        # pre-choice print statements:
        if (pregame_func() if pregame_func else self.pregame_statements()):  # either returns True or None
          continue

        # Play one step of the game.
        winner = self._game.run_one_step()
        if winner:  # game has ended!
          print("{} has won".format(winner))
          break
        # else:  # game is on going. Use this window to ask.
        #   # add post-choice print statements here.
        #   pass

      want_to_play = input("Play again?\n")



if __name__=='__main__':
  # Entry point of the program
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
    sys.exit(1)
  
  # Booleanize them.
  enable_score = False if enable_score == "off" else True
  
  # Construct the base game cli.
  gameCLI = GameCLI(player1, player2, enable_score)

  # If the undo_redo option is enabled. Decorate!
  if undo_redo == "on":
    gameCLI = SaveDecorator(gameCLI)

  # Start the game cli!
  gameCLI.run()