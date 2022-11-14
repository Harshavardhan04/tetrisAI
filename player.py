from board import Direction, Rotation, Shape
from random import Random
from math import log
import time




class Player:
    def choose_action(self, board):
        raise NotImplementedError

class Player1(Player):
    def __init__(self):
        self.q = []
        self.limit = 4
        self.b_count = 0
        self.s_rotations = {
            Shape.I: 2,
            Shape.J: 4,
            Shape.L: 4,
            Shape.O: 1,
            Shape.S: 2,
            Shape.T: 4,
            Shape.Z: 2}

        self.b_count_max = 390
        self.weight1 = 0.2128  
        self.weight2 = 0.85  
        self.weight3 = 5.5  
        self.weight4 = 0.205  
        self.weight5 = 1  
        self.weight6 = 1  
        self.weight7 = 0.5 

    @staticmethod
    def makeQueue(index, shape, alert: bool = False):

        q = []

        if shape != Shape.T and 10 <= index < 30 and not alert:
            q.append(Rotation.Clockwise)
            index = index - 10

        for y in range(abs((index % 10) - 5)):
            if (index % 10) - 5 > 0:
                q.append(Direction.Right)
            elif (index % 10) - 5 < 0:
                q.append(Direction.Left)

        if index//10 == 3:
            q.append(Rotation.Anticlockwise)
        else:
            for y in range(index // 10):
                q.append(Rotation.Clockwise)

        return q

    def popQ(self):
        if len(self.q) > 0:
            move = self.q[0]
            del self.q[0]
            return move

        return Direction.Drop

    @staticmethod
    def rotMove(board, move):
        if board.falling is not None:
            if move == Rotation.Clockwise or move == Rotation.Anticlockwise:
                return board.rotate(move)
            else:
                return board.move(move)
        return

    #gather values for the heurestic

    # gets the max height on the board
    @staticmethod
    def getMaxHeight(board) -> int:
        maxHeight = 23
        for y in board.cells:
            if y[1] < maxHeight:
                maxHeight = y[1]
        return maxHeight

    # get the height of each column
    @staticmethod
    def getHeights(board) -> list:
        heights = [23 for _ in range(10)]

        for x, y in board.cells:
            if y < heights[x]:
                heights[x] = y

        return heights

    # claculate height difference between columns
    @staticmethod
    def getBumpinessLvl(heights: list) -> int:
        bumpiness = 0
        for i in range(9):
            bumpiness += abs(heights[i] - heights[i + 1])
        return bumpiness

    # count holes
    @staticmethod
    def getHoles(board, heights: list, maxHeight: int) -> int:
        bubbles = 0
        for column in range(10):
            for row in range(23, maxHeight - 1, -1):
                if (column, row) not in board.cells and row >= heights[column] < 23:
                    bubbles = bubbles + 1
        return bubbles

    def convertScore(self, score: int) -> float:
        score = score//100  # 100, 400, 800, 1600 -> 1,4,8,16
        if score != 0:
            score = log(score, 2)  # 1, 4, 8, 16 -> 0,2,3,4
            if score == 0:  # since the 100 points converts to 0, we need to increment it to fit the sequence 1,2,3,4
                score += 1

            # we want to discourage smaller combos up until it the end where we need to clear the board.
            if score < self.limit:
                score = ((-1.25) / (score + 1.8))*10.85
            else:
                score = 2**score
                score *= 100

        return score

    @staticmethod
    def getHeight(heights, height):
        for i in range(len(heights)):
            if height == heights[i]:
                return i

    def getMoves(self, board, recurse: bool = True):
        self.q = []
        if recurse:
            self.b_count += 1

        oldHeight = self.getMaxHeight(board)

        try:
            rotationNum = self.s_rotations[board.falling.shape]
        except AttributeError:
            rotationNum = 4

        totalScores = [0 for _ in range(rotationNum * 10)]

        alert = False
        if oldHeight < 6:
            alert = True

        if recurse and oldHeight < 14:
            self.limit = 3

        if self.b_count >= self.b_count_max:
            self.limit = 1
            self.weight5 = 15

        qs = [[] for i in range(rotationNum*10)]
        for rotations in range(rotationNum):
            for position in range(10):
                clone = board.clone()
                index = (rotations * 10) + position

                #15313
                q = self.makeQueue(index, clone.falling, alert)

                for move in q:
                    self.rotMove(clone, move)

                self.rotMove(clone, Direction.Drop)

                raw_score = clone.score - board.score

                score = self.convertScore(raw_score)
                heights = self.getHeights(clone)
                maxHeight = self.getMaxHeight(clone)
                bumpiness = self.getBumpinessLvl(heights)
                bubbles = self.getHoles(clone, heights, maxHeight)
                avgHeight = sum(heights) / 10
                avgDif = abs(maxHeight - avgHeight)

                nextScore = 0

                if recurse:
                    nextScore = self.getMoves(clone, False)

                if avgHeight > 19 and score < 0:
                    avgHeight = 23 - avgHeight

                if clone.alive == False:
                    totalScores[index] = -9000

                totalScores[index] += (maxHeight * self.weight1) + (bumpiness * -self.weight2) + (bubbles * -self.weight3) + \
                                          (avgHeight * self.weight4) + (score * self.weight5) + (nextScore * self.weight6) + \
                                          (avgDif * -self.weight7)

        best_score = max(totalScores)
        index = totalScores.index(best_score)

        if recurse:
            self.limit = 4

        if not recurse:
            return best_score

        self.q = self.makeQueue(index, board.falling, alert)

    def choose_action(self, board):

        for x, y in board.falling.cells:
            if y == 0:
                self.getMoves(board)
                break

        return self.popQ()

SelectedPlayer = Player1
