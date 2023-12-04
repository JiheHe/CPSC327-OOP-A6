from game import Game

class Worker():
  '''The worker that the player controls.'''
  
  WORKER_MOVES = {'n': (-1, 0),  
                  'ne': (-1, 1), 
                  'e': (0, 1), 
                  'se': (1, 1), 
                  's': (1, 0), 
                  'sw': (1, -1), 
                  'w': (0, -1),    # all available build/move directions.
                  'nw': (-1, -1)}  # key: direction, value: (deltaRow, deltaCol) s.t. delta means change.

  def __init__(self, worker_id, start_location):
    self._id = worker_id
    self._current_location = start_location  # worker's location on the board, a tuple of 2 ints
    Game.get_instance().update_worker_location(self._id, self._current_location)  # notify the game instance about the change.

  def _calculate_move(self, location_delta):
    '''
      Compute the resulting location from changing the worker's location by location_delta on the board
      Not actually moving the worker
      Input:
        location_delta - tuple(int, int), the change in index applied to the current location (row_id, col_id)
      Output:
        tuple(int, int) - The resulting location from the change.
    '''
    return (self._current_location[0] + location_delta[0], self._current_location[1] + location_delta[1])
  
  def find_legal_moves(self, action):
    '''
      Enumerate all possible moves of this worker object and find the legal ones
      Input:
        action - str, 'build' for building on and 'move' for moving into
      Output:
        list[str] - legal movement moves from the current worker's position
      NOTE: if you can move, you can definitely build, since you can at least build on
      the location you just left from, which has to be a valid buildable location.
    '''
    legal_moves = []
    for direction, location_delta in Worker.WORKER_MOVES.items():
      new_location = self._calculate_move(location_delta)
      if Game.get_instance().check_new_location_validity(self._current_location, new_location, action):
        legal_moves.append(direction)
        
    return legal_moves
  
  def on_winning_position(self):
    '''
      Check if the worker is on a level 3 building.
      Input:
        None
      Output:
        Boolean - whether the worker is on a level 3 building
    '''
    return Game.get_instance().game_state[self._current_location[0]][self._current_location[1]] == 3
  
  def move(self, direction):
    '''
      Move the worker in the given direction and update its location
      Input:
        str - a LEGAL direction for the worker to move in
      Output:
        tuple(int, int) - the original location of the worker
    '''
    old_location = self._current_location
    self._current_location = self._calculate_move(self.WORKER_MOVES[direction])
    Game.get_instance().update_worker_location(self._id, self._current_location)  # notify the game instance about the change.
    return old_location

  def build(self, direction):
    '''
      Have the worker build in the given direction
      Input:
        str - a LEGAL direction for the worker to build on
    '''
    build_location = self._calculate_move(self.WORKER_MOVES[direction])
    Game.get_instance().game_state[build_location[0]][build_location[1]] += 1  # build!
      
