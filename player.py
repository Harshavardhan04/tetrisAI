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

        # self.b_count_max = 390
        # self.maxHeightWeight = 0.2128  
        # self.bumpinessWeight = 0.85  
        # self.bubbleWeight = 5.5  
        # self.avgHeightWeight = 0.205  
        # self.scoreWeight = 1  
        # self.nextScoreWeight = 1  
        # self.weight7 = 0.5 
        self.b_count_max = 350
        self.maxHeightWeight = 0.2  
        self.bumpinessWeight = 0.9  
        self.bubbleWeight = 5  
        self.avgHeightWeight = 0.105  
        self.scoreWeight = 1  
        self.nextScoreWeight = 1
        self.weight7 = 0.3 
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
            nextMove = self.q[0]
            del self.q[0]
            return nextMove

        return Direction.Drop

    @staticmethod
    def rotMove(board, move):
        if board.falling is not None:
            if move == Rotation.Clockwise or move == Rotation.Anticlockwise:
                return board.rotate(move)
            else:
                return board.move(move)
        

    #gather values for the heurestic

    # gets the max height on the board
    @staticmethod
    def getMaxHeight(board) -> int:
        maxHeight = 23
        for (x,y) in board.cells:
            if y < maxHeight:
                maxHeight = y
        return maxHeight

    def dropBomb(board):
        xIndex = 0
        for (x,y) in board.cells:
            if y > 20:
                xIndex= x
        return xIndex
        
            

    # get the height of each column
    @staticmethod
    def getHeights(board) -> list:
        heights = [23 for _ in range(10)]

        for x, y in board.cells:
            if y < heights[x]:
                heights[x] = y

        return heights

    # calculate height difference between columns
    @staticmethod
    def getBumpinessLvl(heights: list) -> int:
        bumpiness = 0
        for i in range(9):
            bumpiness += abs(heights[i] - heights[i + 1])
        return bumpiness

    # count holes
    @staticmethod
    def getHoles(board, heights: list, maxHeight: int) -> int:
        holesCount = 0
        for x in range(10):
            for y in range(23, maxHeight - 1, -1):
                if (x, y) not in board.cells and y >= heights[x] < 23:
                    holesCount = holesCount + 1
        return holesCount

    def convertScore(self, score: int) -> float:
        modScore = score//100  # 25, 100, 400, 1600 -- > 1,4,16, 64 # 100, 400, 800, 1600 -> 1,4,8,16
        if modScore ==0:# need to increment value to 1 if it's 0
            modScore+=1
        else:
            modScore = log(modScore,2) #4,16,64 -> 2,4,6 
            # we want to discourage smaller combos up until it the end where we need to clear the board.
            if modScore > self.limit:
                modScore = 2**modScore
                modScore *= 100
            else:
                modScore = ((-1.2) / (modScore + 1.85))*11

        return modScore

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
            #self.scoreWeight = 15

        qs = [[] for i in range(rotationNum*10)]
        for rotations in range(rotationNum):
            for xPos in range(10):
                clonedBoard = board.clone()
                index = (rotations * 10) + xPos

                #15313
                q = self.makeQueue(index, clonedBoard.falling, alert)

                for move in q:
                    self.rotMove(clonedBoard, move)

                self.rotMove(clonedBoard, Direction.Drop)

                actualScore = clonedBoard.score - board.score
                scoreConv = self.convertScore(actualScore)
                heights = self.getHeights(clonedBoard)
                maxHeight = self.getMaxHeight(clonedBoard)
                bumpiness = self.getBumpinessLvl(heights)
                holesCount = self.getHoles(clonedBoard, heights, maxHeight)
                avgHeight = sum(heights) / 10


                nextScore = 0

                if recurse:
                    nextScore = self.getMoves(clonedBoard, False)

                if avgHeight > 19 and scoreConv < 0:
                    avgHeight = 23 - avgHeight

                if clonedBoard.alive == False:
                    totalScores[index] = -9000

                totalScores[index] += (maxHeight * self.maxHeightWeight) + (bumpiness * -self.bumpinessWeight) + (holesCount * -self.bubbleWeight) + \
                                          (avgHeight * self.avgHeightWeight) + (scoreConv * self.scoreWeight) + (nextScore * self.nextScoreWeight) 


        topScore = max(totalScores)
        index = totalScores.index(topScore)

        if recurse:
            self.limit = 4

        if not recurse:
            return topScore

        self.q = self.makeQueue(index, board.falling, alert)

    def choose_action(self, board):

        for x, y in board.falling.cells:
            if y == 0:
                self.getMoves(board)
                break

        return self.popQ()

SelectedPlayer = Player1
