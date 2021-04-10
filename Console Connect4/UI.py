from GameRelated import *

class UI:
    def __init__(self, game):
        self._game = game

    def start(self):
        turn = 1
        while True:
            if turn == 1:
                pos = input("Position: ")
                m = self._game.validatePosition(pos)
                if m == None:
                    self._game.movePlayer(int(pos))
                else:
                    print(m)
                    turn = 1 - turn
            else:
                pos, val = self._game._board.minimax(self._game._board._board, 4, True)
                self._game.moveComputer(int(pos))
            print(self._game._board)
            if self._game.gameOver(PLAYER) == True:
                print("Game over! You won")
                break
            elif self._game.gameOver(AI) == True:
                print("Game over! You lost")
                break
            turn = 1 - turn


b = Board()
g = Game(b)
ui = UI(g)
ui.start()
