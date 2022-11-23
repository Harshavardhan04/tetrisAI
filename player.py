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
        self.b_count_max = 375
        self.oldScore=0
        self.nextScore =0
        self.curScore=0

        #Number of rotations for each shape
        self.s_rotations = {
            Shape.I: 2,
            Shape.J: 4,
            Shape.L: 4,
            Shape.O: 1,
            Shape.S: 2,
            Shape.T: 4,
            Shape.Z: 2}

    @staticmethod
    def makeQueue(i, shape, alert: bool = False):

        q = []

        if shape != Shape.T and 10 <= i < 30 and not alert:
            q.append(Rotation.Clockwise)
            i = i - 10

        for y in range(abs((i % 10) - 5)):
            if (i % 10) - 5 > 0:
                q.append(Direction.Right)
            elif (i % 10) - 5 < 0:
                q.append(Direction.Left)

        if i//10 == 3:
            q.append(Rotation.Anticlockwise)
        else:
            for y in range(i // 10):
                q.append(Rotation.Clockwise)

        return q

    def popQ(self):
        if len(self.q) > 0:
            nextMove = self.q[0]
            del self.q[0]
            return nextMove

        return Direction.Drop

    @staticmethod
    def rotMove(board, moveToMake):
        if board.falling is not None:
            if moveToMake == Rotation.Clockwise or moveToMake == Rotation.Anticlockwise:
                return board.rotate(moveToMake)
            else:
                return board.move(moveToMake)

    def dropBomb(board):
        xIndex = 0
        for (x,y) in board.cells:
            if y > 20:
                xIndex= x
        return xIndex    

    #gather values for scoring purpose

    # height of each column
    @staticmethod
    def getHeights(board) -> list:
        heights = [23 for _ in range(10)]
        for x, y in board.cells:
            if y < heights[x]:
                heights[x] = y
        return heights

    @staticmethod
    def getMaxHeight(board) -> int:
        maxHeight = 23
        for (x,y) in board.cells:
            if y < maxHeight:
                maxHeight = y
        return maxHeight

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

    def convertScore(self, board,clonedBoard, score: int) -> float:
        
        modScore = (score)//100  # 25, 100, 400, 1600 -- > 1,4,16, 64 

        if modScore ==0:
            modScore+=1
        else:
            modScore = log(modScore,2) #4,16,64 -> 2,4,6 
            if modScore >= self.limit:
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

        for rotations in range(rotationNum):
            for xPos in range(10):
                clonedBoard = board.clone()
                index = (rotations * 10) + xPos
                q = self.makeQueue(index, clonedBoard.falling, alert)

                for move in q:
                    self.rotMove(clonedBoard, move)
                self.rotMove(clonedBoard, Direction.Drop)

                actualScore = clonedBoard.score - board.score
                scoreConv = self.convertScore(board,clonedBoard,actualScore)
                colHeights = self.getHeights(clonedBoard)
                maxHeight = self.getMaxHeight(clonedBoard)
                bumpiness = self.getBumpinessLvl(colHeights)
                holesCount = self.getHoles(clonedBoard, colHeights, maxHeight)
                avgHeight = sum(colHeights) / 10



                nextScore = 0

                if recurse:
                    nextScore = self.getMoves(clonedBoard, False)


                if clonedBoard.alive == False:
                    totalScores[index] = -8000

                if avgHeight > 19 and scoreConv < 0:
                    avgHeight = 23 - avgHeight

                # totalScores[index] += (maxHeight * 0.2) + (bumpiness * -0.9) + (holesCount * -5) + \
                #                           (avgHeight * 0.105) + (scoreConv * 1) + (nextScore * 1.2) 
                totalScores[index] += (maxHeight * 0.31) + (bumpiness * -0.9) + (holesCount * -5.1) + \
                                          (avgHeight * 0.155) + (scoreConv * 5) + (nextScore * 6) 


        topScore = max(totalScores)
        tsIndex = totalScores.index(topScore)

        if recurse:
            self.limit = 4

        if not recurse:
            return topScore

        self.q = self.makeQueue(tsIndex, board.falling, alert)

    def choose_action(self, board):

        for x, y in board.falling.cells:
            if y == 0:
                self.getMoves(board)
                break
        return self.popQ()

SelectedPlayer = Player1


