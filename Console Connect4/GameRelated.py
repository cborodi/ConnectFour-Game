from Board import *

class Game:
    def __init__(self, board):
        self._board = board

    def isNumber(self, number):
        try:
            int(number)
        except:
            return False
        return True

    def validatePosition(self, position):
        if not self.isNumber(position):
            return "Position must be a number"
        position = int(position)
        if position < 0 or position > 6:
            return "Position must be between 0 and 6"
        if self._board.validLocation(position) == False:
            return "That column is full"
        return None

    def movePlayer(self, position):
        x = self._board.findRow(position)
        self._board.placePiece(x, position, PLAYER)

    def moveComputer(self, position):
        x = self._board.findRow(position)
        self._board.placePiece(x, position, AI)

    def bestPosition(self, piece):
        return self._board.pickBestPosition(piece)

    def gameOver(self, piece):
        return self._board.gameWon(piece) or self._board.gameTie()
