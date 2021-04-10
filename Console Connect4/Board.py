
from texttable import Texttable
import random

ROWS = 6
COLS = 7

PLAYER = -1
AI = 1

class Board:
    def __init__(self):
        self._board = [[0]*COLS, [0]*COLS, [0]*COLS, [0]*COLS, [0]*COLS, [0]*COLS]
        self._moves = 0

    def validLocation(self, position):
        if self._board[ROWS-1][position] == 0:
            return True
        return False

    def validLocations(self):
        li = []
        for i in range(COLS):
            if self.validLocation(i) == True:
                li.append(i)
        return li

    def findRow(self, position):
        for i in range(ROWS):
            if self._board[i][position] == 0:
                return i

    def findRowForBoard(self, board, position):
        for i in range(ROWS):
            if board[i][position] == 0:
                return i

    def placePiece(self, x, y, piece):
        self._board[x][y] = piece
        self._moves += 1

    def gameWon(self, piece):
        for i in range(ROWS):
            for j in range(COLS-3):
                if self._board[i][j] == piece and self._board[i][j+1] == piece and self._board[i][j+2] == piece and self._board[i][j+3] == piece:
                    return True

        for i in range(ROWS-3):
            for j in range(COLS):
                if self._board[i][j] == piece and self._board[i+1][j] == piece and self._board[i+2][j] == piece and self._board[i+3][j] == piece:
                    return True

        for i in range(ROWS-3):
            for j in range(COLS-3):
                if self._board[i][j] == piece and self._board[i+1][j+1] == piece and self._board[i+2][j+2] == piece and self._board[i+3][j+3] == piece:
                    return True

        for i in range(ROWS-3):
            for j in range(COLS-1, 2, -1):
                if self._board[i][j] == piece and self._board[i+1][j-1] == piece and self._board[i+2][j-2] == piece and self._board[i+3][j-3] == piece:
                    return True
        return False

    def gameWonForBoard(self, board, piece):
        for i in range(ROWS):
            for j in range(COLS-3):
                if board[i][j] == piece and board[i][j+1] == piece and board[i][j+2] == piece and board[i][j+3] == piece:
                    return True

        for i in range(ROWS-3):
            for j in range(COLS):
                if board[i][j] == piece and board[i+1][j] == piece and board[i+2][j] == piece and board[i+3][j] == piece:
                    return True

        for i in range(ROWS-3):
            for j in range(COLS-3):
                if board[i][j] == piece and board[i+1][j+1] == piece and board[i+2][j+2] == piece and board[i+3][j+3] == piece:
                    return True

        for i in range(ROWS-3):
            for j in range(COLS-1, 2, -1):
                if board[i][j] == piece and board[i+1][j-1] == piece and board[i+2][j-2] == piece and board[i+3][j-3] == piece:
                    return True
        return False

    def findSpace(self, col):
        for r in range(ROWS):
            if self._board[r][col] == 0:
                return r

    def evaluate_position(self, window, piece):
        opponent_piece = PLAYER
        if piece == PLAYER:
            opponent_piece = AI
        score = 0
        if window.count(piece) == 4:
            score += 1000
        elif window.count(piece) == 3 and window.count(0) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(0) == 2:
            score += 2

        if window.count(opponent_piece) == 3 and window.count(0) == 1:
            score -= 100
        elif window.count(opponent_piece) == 2 and window.count(0) == 2:
            score -= 3

        return score

    def calculateScore(self, newBoard, piece):
        score = 0

        center_array = [int(newBoard[i][COLS//2]) for i in range(ROWS)]
        center_pieces = center_array.count(piece)
        score += center_pieces * 3

        for r in range(ROWS):
            row_array = [int(newBoard[r][i]) for i in range(COLS)]
            for c in range(COLS-3):
                window = row_array[c:c+4]
                score += self.evaluate_position(window, piece)

        for c in range(COLS):
            col_array = [int(newBoard[i][c]) for i in range(ROWS)]
            for r in range(ROWS-3):
                window = col_array[r:r+4]
                score += self.evaluate_position(window, piece)

        for r in range(ROWS-3):
            for c in range(COLS-3):
                window = [newBoard[r+i][c+i] for i in range(4)]
                score += self.evaluate_position(window, piece)

        for r in range(ROWS-3):
            for c in range(COLS-1, 2, -1):
                window = [newBoard[r+i][c-i] for i in range(4)]
                score += self.evaluate_position(window, piece)

        return score

    def pickBestPosition(self, piece):
        possible_locations = self.validLocations()
        best_score = -1000000
        best_column = random.choice(possible_locations)
        for col in possible_locations:
            row = self.findSpace(col)
            newBoard = []
            for e in self._board:
                newBoard.append(list(e))

            newBoard[row][col] = piece

            score = self.calculateScore(newBoard, piece)
            if score > best_score:
                best_score = score
                best_column = col
        return best_column

    def gameTie(self):
        return self._moves == ROWS * COLS

    def isTerminal(self, board):
        return self.gameWonForBoard(board, PLAYER) or self.gameWonForBoard(board, AI) or self.gameTie()

    def minimax(self, board, depth, maximizingPlayer):
        possible_locations = self.validLocations()
        terminal = self.isTerminal(board)
        if depth == 0 or terminal:
            if terminal:
                if self.gameWonForBoard(board, PLAYER):
                    return None, -10000000
                elif self.gameWonForBoard(board, AI):
                    return None, 10000000
                else:
                    return None, 0
            else:
                return None, self.calculateScore(board, AI)
        if maximizingPlayer:
            value = -1000000000000
            column = random.choice(possible_locations)
            for col in possible_locations:
                row = self.findRowForBoard(board, col)
                if row != None:
                    newBoard = []
                    for e in board:
                        newBoard.append(list(e))
                    newBoard[row][col] = AI
                    new_score = self.minimax(newBoard, depth-1, False)[1]
                    if new_score > value:
                        value = new_score
                        column = col
            return column, value
        else:
            value = 1000000000000
            column = random.choice(possible_locations)
            for col in possible_locations:
                row = self.findRowForBoard(board, col)
                if row != None:
                    newBoard = []
                    for e in board:
                        newBoard.append(list(e))
                    newBoard[row][col] = PLAYER
                    new_score = self.minimax(newBoard, depth-1, True)[1]
                    if new_score < value:
                        value = new_score
                        column = col
            return column, value


    def __str__(self):
        t = Texttable()
        for i in range(ROWS-1, -1, -1):
            d = {PLAYER:'X', 0:' ', AI:'Y'}
            row = list(self._board[i])
            for j in range(COLS):
                row[j] = d[row[j]]
            t.add_row(row)
        return t.draw()


