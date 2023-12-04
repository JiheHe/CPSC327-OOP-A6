from game import Game

if __name__=='__main__':
  test = Game("human", "heuristic", None, None)
  # test2 = Game(True, True, False, False)
  # print(test2)
  print(test)
  test._players[0]._workers['A'].move('n')
  print(test)
