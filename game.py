class Game:
  '''
    The game object that runs an ongoing instance of Santorini.
    The "Originator" of the Memento Design Pattern.
    The Game 'Singleton' of the Singleton Design Pattern (uses __new__ over __init__)
  '''

  #--------------------------------------------SINGLETON PORTION START --------------------------------------------#
  '''Singleton is applied for the ease of access here, rather than reducing duplicates, so might not seem as necessary.'''

  _instance = None  # the singleton game instance

  # NOTE: self works here, no need to @classmethod it. cls by convention.
  def __new__(cls, p1_type, p2_type, undo_redo, score_display):  # TODO: add more arguments to fit the design later.
      '''With the current singleton logic, every time the object initialization is called, the object gets reset.
      This is valid since __new__ can be only accessed like __init__ and nowhere else. Again, for the ease of reference.'''
      # Sets up the singleton if not yet. The setup below only need to run once.
      if not cls._instance:
          cls._instance  = super(Game, cls).__new__(cls)  # avoids self-looping when setting up an instance of self class.
          # Sets up player agents with correct types. Only need to init once since same agents throughout.
          cls._instance._players = [
              cls._instance._create_player_agent(p1_type, "white"),
              cls._instance._create_player_agent(p2_type, "blue"),]
          # Have decorator stuff here.

      # Sets up (or resets) the initial game state
      cls._instance._initialize_gameboard()

      return cls._instance

  @classmethod
  def get_instance(cls):
      '''The getter method that returns the current Singleton Game instance'''
      # NOTE: no need to check for _instance & new if None, since our logic guarantees the existence of a game object
      # at the beginning. Again, singleton is only used for ease of reference here, not duplication reduction.
      return cls._instance
  #--------------------------------------------SINGLETON PORTION END--------------------------------------------#
  

  def _initialize_gameboard(self):
    '''
      NOTE: define the coordinate system of the board as: 
      order- (row, col), (0, 0) top-left, (5, 5) bottom-right
    '''
    # represent the gameboard and building levels as a 2D array of integers such that 0-3 represents the levels, and -1 represents a dome
    self._game_state = [[0 for j in range(5)] for i in range(5)]  # initialize to initial board state
    # represent the worker placements as a dictionary of tuples s.t. the key is worker's letter, and the value is the worker's location
    self._worker_locations = {}  # a dictionary of tuples, a READ-ONLY update board of locations.

    for player in self._players:   # initialize to initial worker locations
      player.initialize_workers()

    # represent the index of the player with the current turn in _players
    self._turn_index = 0  # starts with player 1

  def _get_game_state(self):
      '''The getter method that returns the _game_state object'''
      return self._game_state
  game_state = property(_get_game_state)  # for ease of publically-accessing notation

  def update_worker_location(self, worker_id, new_location):
    '''
      The setter method that notifies the game to update worker location. This way we avoid exposing _workers and _locations
      Input:
        worker_id - str, the letter representation of worker's identity
        new_location - tuple(int, int), the new location of the worker on the board
    '''
    self._worker_locations[worker_id] = new_location

  def _create_player_agent(self, type, color):
    from player import HumanPlayer, RandomPlayer, HeuristicPlayer  # using lazy import to avoid interdependency
    if type == "human":
      return HumanPlayer(color)
    elif type == "heuristic":
      return HeuristicPlayer(color)
    elif type == "random":
      return RandomPlayer(color)

  def check_new_location_validity(self, old_location, new_location, action):
    '''
      Check if the supplied location is a valid new location for the worker to move into, or build on
      Input:
        old_location - tuple(int, int), the old location (row_id, col_id) the worker is currently at
        new_location - tuple(int, int), the new location (row_id, col_id) the worker is moving into or building on
        action - str, 'build' for building on and 'move' for moving into
      Output:
        bool - True if location is valid for the action, False otherwise
    '''
 
    board_size = 5
    # height of current location
    level = self._game_state[old_location[0]][old_location[1]]
    row, col = new_location[0], new_location[1]

    # check if new location is outside of bounds
    if row < 0 or row >= board_size or col < 0 or col >= board_size:
      return False

    # check if new location is occupied by a worker
    if (row, col) in self._worker_locations.values():
       return False

    # level mismatch only for movement, bounded by level + 1
    if action == "move" and self._game_state[row][col] > level + 1:
       return False

    return True


  def __str__(self):
    '''the board representation used for CLI'''
    # Update the board into a print state by fusing in workers
    board_to_print = [[str(self._game_state[i][j]) + ' ' for j in range(5)] for i in range(5)]
    for worker_id, location in self._worker_locations.items():
      board_to_print[location[0]][location[1]] = board_to_print[location[0]][location[1]][0] + worker_id  # update the space with worker id at correct locations
    # Print the board
    board_representation = ""
    for row in range(5):
      board_representation += "+--+--+--+--+--+\n"
      for col in range(5):
         board_representation += "|" + board_to_print[row][col]
      board_representation += "|\n"
    board_representation += "+--+--+--+--+--+"
    return board_representation

  def _next_turn(self):
    self._turn_index = 0 if self._turn_index else 1

  def run(self):
    # while game is not over, players move
    while True:
      result = self._players[self._turn_index].execute_round()
      if result != "none":
        break
      # iterator
      self._next_turn()
    
    # get winner and print winner
    # winner = self._players[(self._turn_index + (result == "lose")) % 2]
    if result == "winner":
      winner = self._players[self._turn_index]
    else:
      winner = self._players[(self._turn_index + 1) % 2]

    print("{} has won".format(winner))



# Note: I hate running test in this... wasn't even a bug... just main stuff.