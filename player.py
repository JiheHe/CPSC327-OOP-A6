import abc
from game import Game 
from worker import Worker
import random

class Player(metaclass=abc.ABCMeta):  
  '''
    Declare an interface common to all Player type behaviors. Game uses this interface 
    to call the behavior defined by a concrete TypePlayer.
    The 'Abstract Parent' of the Template Method Design Pattern.
    NOTE: an abstract class isn't necessary in Python, but this is good for bookkeeping.
    NOTE: can have state variables and concrete functions in the abstract class
  '''

  def __init__(self, color):
    self._color = color
  
  def initialize_workers(self):
    '''Reset the worker objects to their default positions through reinitialization'''
    # Too insignificant of a check to insert a new pattern.
    if self._color == 'white':
      self._workers = {'A': Worker('A', (3, 1)), 'B': Worker('B', (1, 3))}
    elif self._color == 'blue':
      self._workers = {'Y': Worker('Y', (1, 1)), 'Z': Worker('Z', (3, 3))}

  def execute_round(self):
    '''Execute a round of decision and movement for this player'''
    result = self._check_game_ongoing()
    if result == "win":  # this player won the game
      # TODO: print and prompt
      pass
    elif result == "lose":  # this player lost the game
      # TODO: print and prompt
      pass
    else: # ongoing, result is a set of moves
      self._make_decision(result)
      
  def _check_game_ongoing(self):
    for worker in self._workers.values():
      if worker.on_winning_position():
        return "win"
    moves = []
    for id, worker in self._workers.items():
      moves += [(id, move) for move in worker.find_legal_moves("move")]  # attach with worker id identifier.
    if len(moves) == 0:  # no legal moves available
      return "lose"
    return set(moves)
      
  @abc.abstractmethod
  def _make_decision(self, legal_moves):
    '''
      Make a decision on which worker to move to where and build where for this step, then carry it out.
      Input:
        legal_moves - a non-empty set of (str, str), each representing a unique legal (worker_id, move)
      Output:
        None
    '''
    pass


class HumanPlayer(Player):
  '''Implement the interactive human Player using the Player interface.'''

  def _make_decision(self, legal_moves):
    # TODO: prompt user input, maybe through a subscriber model in CLI
    pass

class RandomPlayer(Player):
  '''Implement the automated random AI Player using the Player interface.'''
  
  def _make_decision(self, legal_moves):
    '''Randomly choose a move from the set of allowed moves'''
    worker_id, direction = random.choice(legal_moves)
    self._workers[worker_id].move(direction)  # update the worker location with legal move
    build_direction = random.choice(set(self._workers[worker_id].find_legal_moves("build")))  # at least 1 exists
    self._workers[worker_id].build(build_direction)  # build a level there

class HeuristicPlayer(Player):
  '''Implement the automated heuristic AI Player using the Player interface.'''
  
  def _make_decision(self, legal_moves):
    # TODO:
    pass