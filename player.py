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
  
  def __str__(self):
    return self._color
  
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
    if isinstance(result, str):
      return result  # either "win" or "lose"
    else: # ongoing, result is a set of moves
      self._make_decision(result)
      return None
      
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
    # look at each available move, calculates a move_score, and pick the highest one, breaking any ties randomly.
    for worker_id, direction in legal_moves:
      # cache the old location, move to new location
      original_location = self._workers[worker_id].move(direction)

      # height score: the sum of the heights of the buildings a player's workers stand on.
      height_score = 0
      # center_score: how close the worker is from the center ring
      center_score = 0
      # distance_score: the sum of the minimum distance to the opponent's workers
      distance_score = 0
      opponent_workers = ['Y', 'Z'] if (self._color == "white") else ['A', 'B']

      for worker_id in self._workers.keys():
        worker_location = Game.get_instance().get_worker_location(worker_id)

        # height score
        level = Game.get_instance().game_state[worker_location[0]][worker_location[1]]
        height_score += 99999 if level == 3 else level  # level == 3 is win!!! big reward

        # center score
        if worker_location == (2, 2): # center space
          center_score += 2
        if abs(worker_location[0] - 2) <= 1 and abs(worker_location[1] - 2) <= 1:  # middle ring
          center_score += 1

        # distance score
        for opponent_worker_id in opponent_workers:
          opponent_worker_location = Game.get_instance().get_worker_location(opponent_worker_id)

          # Check code and implement
      
      

      # restore to old location


    pass