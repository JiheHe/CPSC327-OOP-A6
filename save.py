from abc import ABC, abstractmethod
from copy import deepcopy

class Save(ABC):
  '''
    The Memento interface provides a way to retrieve the memento's metadata, such as creation date or name. 
    However, it doesn't expose the Originator's state.
    The "Abstract Memento" of the Memento Design Pattern.
  '''
  
  @abstractmethod
  def get_overall_game_state(self):
    pass

class GameSave(Save):
  '''
    The "Concrete Memento" of the Memento Design Pattern.
  '''
  def __init__(self, game_state: list, worker_locations: dict, players: list, turn_index: int):
    # Create deep copies of the mutable objects; else they'll be saved by reference!
    # RIP memory.
    self._game_state = deepcopy(game_state)  # a list of list of int
    self._worker_locations = deepcopy(worker_locations)  # a dictionary of tuples
    self._players = deepcopy(players)  # a list of Player objects (deepcopy does recursive copying so Workers are copied too)
    self._turn_index = turn_index  # an int

  def get_overall_game_state(self):
    """
      The Originator Game uses this method when restoring its state.
    """
    return self._game_state, self._worker_locations, self._players, self._turn_index
    
