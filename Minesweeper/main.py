from random import randint
import os
from collections import deque


class Cell:
    def __init__(self, val: int):
        self.__val = val

        self.__isFlagged = False
        self.__isMined = False

    def isMine(self):
        return self.__val == -1

    def hasBeenMined(self):
        return self.__isMined

    def hasBeenFlagged(self):
        return self.__isFlagged

    def flag(self):
        self.__isFlagged = not self.__isFlagged

    def mine(self):
        if self.__isMined or self.__isFlagged:
            return False

        self.__isMined = True
        return self.isMine()

    def getVal(self):
        return self.__val

    def incrementVal(self):
        self.__val += 1


class Board:
    def __init__(self, size):
        self.__size = size
        self.__board = [[None for _ in range(size)] for _ in range(size)]
        self.mines = 0

    def size(self):
        return self.__size

    def generateBoard(self, startR, startC):
        self.mines = 0
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]
        noMineTiles = [(startR + dR, startC + dC) for dR, dC in directions]
        noMineTiles.append((startR, startC))

        for i in range(self.__size):
            for j in range(self.__size):
                isMine = randint(1, 5) == 1

                if not isMine or (i, j) in noMineTiles:
                    if not self.__board[i][j]:
                        self.__board[i][j] = Cell(0)

                    continue

                self.mines += 1
                self.__board[i][j] = Cell(-1)

                for d in directions:
                    newI = i + d[0]
                    newJ = j + d[1]

                    if newI < 0 or newI >= self.__size or newJ < 0 or newJ >= self.__size:
                        continue

                    if not self.__board[newI][newJ]:
                        self.__board[newI][newJ] = Cell(0)

                    if not self.__board[newI][newJ].isMine():
                        self.__board[newI][newJ].incrementVal()

        res = 0
        for r, c in noMineTiles:
            _, b = self.mine(r, c)
            res += b

        return res

    def toString(self):
        res = "   " + "  ".join([str(i) for i in range(self.__size)]) + "\n"

        for r in range(self.__size):
            curr = str(r) + "  "
            for col in self.__board[r]:
                curr += str(col.getVal()) + "  " if col.hasBeenMined() else ("F  " if col.hasBeenFlagged() else "*  ")

            res += curr + "\n"

        return res

    def flag(self, row, col):
        self.__board[row][col].flag()

    def mine(self, row, col):
        if self.__board[row][col].hasBeenMined():
            return False, 0

        if self.__board[row][col].getVal() == 0:
            self.__board[row][col].mine()
            return False, self.floodFill(row, col) + 1

        return self.__board[row][col].mine(), 1

    def floodFill(self, row, col):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]

        queue = deque([(row, col)])
        res = 0

        while queue:
            r, c = queue.popleft()

            for dR, dC in directions:
                nR = r + dR
                nC = c + dC

                if 0 <= nR < self.__size and 0 <= nC < self.__size:
                    if self.__board[nR][nC].getVal() == 0 and not self.__board[nR][nC].hasBeenMined():
                        queue.append((nR, nC))

                    if not self.__board[nR][nC].hasBeenMined():
                        self.__board[nR][nC].mine()
                        res += 1

        return res



class Game:
    def __init__(self, board, initialScore):
        self.__board = board
        self.__playing = False
        self.score = initialScore
        self.target = self.__board.size() ** 2 - self.__board.mines

    def play(self):
        self.__playing = True

        while self.__playing:
            self.playTurn()

    def playTurn(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Current score: ", self.score)
        print("Target score: ", self.target)

        print("Current Board:")
        print(self.__board.toString())

        row = self.askForNumber("Enter a ROW NUMBER: ", self.__board.size())
        col = self.askForNumber("Enter a COLUMN NUMBER: ", self.__board.size())

        thing = self.askForInput("Enter F for flag or M for mine: ", lambda x: x in ["F", "M"])

        if thing == "F":
            self.__board.flag(row, col)
            return

        res, more = self.__board.mine(row, col)

        if res:
            self.gameOver()
        else:
            self.score += more

        if self.score >= self.target:
            self.winGame()

    def askForInput(self, message, validator=lambda x: False):
        res = input(message)

        while not validator(res):
            res = input(message)

        return res

    def askForNumber(self, message, upper=float('inf'), lower=0):
        while True:
            try:
                res = int(input(message))
                if lower <= res <= upper:
                    return res
            except ValueError as e:
                continue

    def gameOver(self):
        print("GAME OVER!!!!!!!!!!!!")
        self.__playing = False

    def winGame(self):
        print("GAME WON!!!!!!!!!!! YAAYYYYYYYYYYYYYYYYYYYYYYYYYY!!!!!!!!!!!!!!!!!!111")
        self.__playing = False


if __name__ == "__main__":
    board = Board(10)

    input("--- PRESS ENTER TO START ---")

    res = board.generateBoard(5, 5)
    game = Game(board, res)
    game.play()
