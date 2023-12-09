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
    return moves
      
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
    workers = ["A", "B", "Y", "Z"]

    # select worker
    worker_id = ""
    while worker_id not in self._workers:
      worker_id = input("Select a worker to move\n")
      if worker_id not in workers:
        print("Not a valid worker")
      elif worker_id not in self._workers:
        print("That is not your worker")
    worker = self._workers[worker_id] # needed

    # select direction and move
    direction = ""
    while direction not in worker.find_legal_moves('move'):
      direction = input("Select a direction to move (n, ne, e, se, s, sw, w, nw)\n")
      if direction not in Worker.WORKER_MOVES:
        print("Not a valid direction")
      elif direction not in worker.find_legal_moves('move'):
        print("Cannot move {}".format(direction))
    
    worker.move(direction)

    # selection where to build
    build = ""
    while build not in worker.find_legal_moves('build'):
      build = input("Select a direction to build (n, ne, e, se, s, sw, w, nw)\n")
      if build not in Worker.WORKER_MOVES:
        print("Not a valid direction")
      elif build not in worker.find_legal_moves('build'):
        print("Cannot build {}".format(build))
    
    worker.build(build)

    print(f"{worker_id},{direction},{build}")  # print the User's choice!

class RandomPlayer(Player):
  '''Implement the automated random AI Player using the Player interface.'''
  
  def _make_decision(self, legal_moves):
    '''Randomly choose a move from the set of allowed moves'''
    worker_id, direction = random.choice(legal_moves)
    self._workers[worker_id].move(direction)  # update the worker location with legal move
    build_direction = random.choice(self._workers[worker_id].find_legal_moves("build"))  # at least 1 exists
    self._workers[worker_id].build(build_direction)  # build a level there

    print(f"{worker_id},{direction},{build_direction}")  # print the User's choice!

class HeuristicPlayer(Player):
  '''Implement the automated heuristic AI Player using the Player interface.'''
  
  def _make_decision(self, legal_moves):
    # look at each available move, calculates a move_score, and pick the highest one, breaking any ties randomly.
    # then build randomly after (as answered on Ed)

    # NOTE (important):
    # Does the distance refer to 2D distance, or does height count as well?

    max_move_score_moves = []  # the cache during the calculation
    max_move_score = None  # the running max

    for worker_id, direction in legal_moves:
      # cache the old location, move to new location
      original_location = self._workers[worker_id].move(direction)

      # height score: the sum of the heights of the buildings a player's workers stand on.
      height_score = 0
      # center_score: how close the worker is from the center ring
      center_score = 0

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

      # distance_score: the sum of the minimum distance to the opponent's workers
      distance_score = 0
      opponent_workers = ['Y', 'Z'] if (self._color == "white") else ['A', 'B']

      for opponent_worker_id in opponent_workers:
        opponent_worker_location = Game.get_instance().get_worker_location(opponent_worker_id)

        # Going to use L1 distance as the distance metric.
        # List comprehension of formula. Ex. # Ex. for blue, it would be min(distance from Z to A, distance from Y to A) + min(distance from Z to B, distance from Y to B)
        distance_score += min( [ abs(opponent_worker_location[0]-worker_location[0]) + abs(opponent_worker_location[1]-worker_location[1])
           for worker_location in [Game.get_instance().get_worker_location(worker_id) for worker_id in self._workers.keys()] ] )

      # parameter weights
      c1 = 3
      c2 = 2
      c3 = 1

      # calculuate the total move score
      move_score = c1 * height_score + c2 * center_score + c3 * distance_score

      # append the result to the cache, if it's a max
      if not max_move_score:  # first value, the initial baseline
        max_move_score = move_score
        max_move_score_moves.append((worker_id, direction))
      else:
        if move_score > max_move_score:
          max_move_score = move_score
          max_move_score_moves = [(worker_id, direction)]  # resets the cache
        elif move_score == max_move_score:
          max_move_score_moves.append((worker_id, direction))  # a valid option
      
      # restore to old location
      self._workers[worker_id].move(original_location)

    # Pick the move that has the maximum move_score (break tie randomly)
    worker_id, direction = random.choice(max_move_score_moves)
    
    # Move the chosen worker to the chosen location (execute the chosen move)
    self._workers[worker_id].move(direction)

    # Build randomly (yes copy+paste same 2 lines of code from random. But only copied here so should be fine.)
    build_direction = random.choice(self._workers[worker_id].find_legal_moves("build"))  # at least 1 exists
    self._workers[worker_id].build(build_direction)  # build a level there

    print(f"{worker_id},{direction},{build_direction}")  # print the User's choice!