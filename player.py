from board import Direction, Rotation, Action, Block, Board, Shape
from random import Random
import time




class Player:
    def choose_action(self, board):
        raise NotImplementedError


class RandomPlayer(Player):
    def __init__(self, seed=None):

        self.random = Random(seed)

    def print_board(self, board):
        print("--------")
        for y in range(24):
            s = ""
            for x in range(10):
                if (x,y) in board.cells:
                    s += "#"
                else:
                    s += "."
            print(s, y)
                

            

    def choose_action(self, board):
        #self.print_board(board)
        time.sleep(0.5)
        if self.random.random() > 0.97:
            # 3% chance we'll discard or drop a bomb
            return self.random.choice([
                Action.Discard,
                Action.Bomb,
            ])
        else:
            # 97% chance we'll make a normal move
            return self.random.choice([
                Direction.Left,
                Direction.Right,
                Direction.Down,
                Rotation.Anticlockwise,
                Rotation.Clockwise,
            ])

class Player1(Player):
    prev =0
    prevI=0


    def __init__(self, seed=None):
        self.random = Random(seed)

    def print_board(self, board):
        print("--------")
        for y in range(24):
            s = ""
            for x in range(10):
                if (x,y) in board.cells:
                    s += "#"
                else:
                    s += "."
            print(s, y)

    def score_board(self,board):
        maxYoccupied = max(y for (x,y) in board.cells)
        heightScore = (1/maxYoccupied)*100
        totalScore = board.score+heightScore
        return totalScore

    def possible_moves(self, board):
        for pos in range(10):
            print(isinstance(board, Board))
            curX = board.falling.left
            break
        self.move_towards_target(pos,curX,board)
        
    def choose_action(self, board):
        moves=[]
        if board.falling.shape == Shape.I:
                if self.prevI ==0:
                    self.prevI =1
                    for i in range(board.falling.left):
                        moves.append(Direction.Left)
                elif self.prevI==1:
                    self.prevI = 0
                    dif = 9-board.falling.left
                    for i in range(dif):
                        moves.append(Direction.Right)
        else:
            if self.prev ==0:
                self.prev=1
                dif = board.falling.left-1
                for i in range(dif):
                    moves.append(Direction.Left)
            elif self.prev ==1:
                self.prev=2
                dif = 4-board.falling.left
                for i in range(dif):
                    moves.append(Direction.Left)
            elif self.prev ==2:
                self.prev=0
                dif = 6-board.falling.left
                for i in range(dif):
                    moves.append(Direction.Right)
        moves.append(Direction.Drop)
        return moves
        



SelectedPlayer = Player1
