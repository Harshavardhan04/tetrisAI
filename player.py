# from board import Direction, Rotation, Action, Block, Board, Shape
# from random import Random
# import time




# class Player:
#     def choose_action(self, board):
#         raise NotImplementedError


# class RandomPlayer(Player):
#     def __init__(self, seed=None):

#         self.random = Random(seed)

#     def print_board(self, board):
#         print("--------")
#         for y in range(24):
#             s = ""
#             for x in range(10):
#                 if (x,y) in board.cells:
#                     s += "#"
#                 else:
#                     s += "."
#             print(s, y)
                

            

#     def choose_action(self, board):
#         #self.print_board(board)
#         time.sleep(0.5)
#         if self.random.random() > 0.97:
#             # 3% chance we'll discard or drop a bomb
#             return self.random.choice([
#                 Action.Discard,
#                 Action.Bomb,
#             ])
#         else:
#             # 97% chance we'll make a normal move
#             return self.random.choice([
#                 Direction.Left,
#                 Direction.Right,
#                 Direction.Down,
#                 Rotation.Anticlockwise,
#                 Rotation.Clockwise,
#             ])

# class Player1(Player):
#     prev =0
#     prevI=0


#     def __init__(self, seed=None):
#         self.random = Random(seed)

#     def print_board(self, board):
#         print("--------")
#         for y in range(24):
#             s = ""
#             for x in range(10):
#                 if (x,y) in board.cells:
#                     s += "#"
#                 else:
#                     s += "."
#             print(s, y)

#     def score_board(self,board):
#         maxYoccupied = max(y for (x,y) in board.cells)
#         heightScore = (1/maxYoccupied)*100
#         totalScore = board.score+heightScore
#         return totalScore

#     def possible_moves(self, board):
#         for pos in range(10):
#             print(isinstance(board, Board))
#             curX = board.falling.left
#             break
#         self.move_towards_target(pos,curX,board)
        
#     def choose_action(self, board):
#         moves=[]
#         if board.falling.shape == Shape.I:
#                 if self.prevI ==0:
#                     self.prevI =1
#                     for i in range(board.falling.left):
#                         moves.append(Direction.Left)
#                 elif self.prevI==1:
#                     self.prevI = 0
#                     dif = 9-board.falling.left
#                     for i in range(dif):
#                         moves.append(Direction.Right)
#         else:
#             if self.prev ==0:
#                 self.prev=1
#                 dif = board.falling.left-1
#                 for i in range(dif):
#                     moves.append(Direction.Left)
#             elif self.prev ==1:
#                 self.prev=2
#                 dif = 4-board.falling.left
#                 for i in range(dif):
#                     moves.append(Direction.Left)
#             elif self.prev ==2:
#                 self.prev=0
#                 dif = 6-board.falling.left
#                 for i in range(dif):
#                     moves.append(Direction.Right)
#         moves.append(Direction.Drop)
#         return moves
        



# SelectedPlayer = Player1
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
    I_tracker = 0
    T_tracker = 1
    next_piece_T = 0
    L_tracker = 0
    next_piece_L = 0
    J_tracker = 1
    next_piece_J = 0
    O_tracker = 0
    Z_tracker = 0
    next_piece_Z = 0
    prev =0
    prev2=0
    future_move = []


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

    # def move_towards_target(self,pos,curX,board):
    #     if pos>curX:
    #         dif = pos-curX
    #         for i in range(0,dif):
    #             board.move(Direction.Right)
    #     else:
    #         dif = curX-pos
    #         for i in range(0,dif):
    #             board.move(Direction.Left)
    #     board.move(Direction.Drop)

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
                #print(self.score_board(board))

    def moveBlock(self,board):
        heightScore=0
        totalScore=0
        moves = []
        listForScoring = []
        tempMovesList = []
        topScore=0
        for i in range(10):
            sandbox = board.clone()
            if i>sandbox.falling.left:
                dif = i-sandbox.falling.left
                for j in range(dif):
                    sandbox.move(Direction.Right)
                    tempMovesList.append(Direction.Right)
                    print(sandbox.falling.left)
                sandbox.move(Direction.Drop)
            elif i <sandbox.falling.left:
                dif = sandbox.falling.left-i
                for j in range(dif):
                    sandbox.move(Direction.Left)
                    tempMovesList.append(Direction.Left)
                sandbox.move(Direction.Drop)
            else:
                print("huh")
                sandbox.move(Direction.Drop)
        
            
            #print("Temp Moves List: ",listForScoring)
            maxYoccupied = max(y for (x,y) in sandbox.cells)
            heightScore = (1/maxYoccupied)*100
            totalScore = sandbox.score+heightScore
            if totalScore>topScore:
                print("this does get called")
                topScore = totalScore
                print("Top Score: ",topScore)
                listForScoring.clear()
                listForScoring.extend(tempMovesList)
            else:
                continue
        # for item in listForScoring:
        #     yield item
        # print(listForScoring)
        
    

    def choose_action(self, board):
            moves=[]
            heightLeft = 0
            heightRight=0
            height = 0
            # for y in range (20,board.height):
            #     for x in range (board.width):
            #         if (x, y) in board.cells:
            #             moves.append(Action.Bomb)
        # else:
            if self.next_piece_Z==1:
                if board.falling.shape == Shape.Z:
                    moves.extend(self.future_move)

            elif board.falling.shape == Shape.I:
                # for (x,y) in board.cells:
                #         if x ==0:
                #             if y > heightLeft:
                #                 heightLeft = y
                #         elif x==9:
                #             if y > heightRight:
                #                 heightRight = y
                if self.I_tracker==0:
                    self.I_tracker=1
                    dif = board.falling.left
                    # if heightLeft > 20:
                    #     dif = dif - 1
                    for i in range(dif):
                        moves.append(Direction.Left)
                elif self.I_tracker==1:
                    self.I_tracker=2
                    dif = 9-board.falling.left
                    # if heightRight > 20:
                    #     dif = dif-1
                    for i in range(dif):
                        moves.append(Direction.Right)
                elif self.I_tracker==2:
                    self.I_tracker=0
                    dif = 6-board.falling.left
                    for i in range(dif):
                        moves.append(Direction.Right)
                    
            elif board.falling.shape == Shape.T:
                if self.T_tracker==0:
                    self.T_tracker=1
                    moves.append(Rotation.Anticlockwise)
                    dif = board.falling.left
                    for i in range(dif):
                        moves.append(Direction.Left)
                    if board.next.shape == Shape.Z:
                        self.next_piece_Z=1
                        self.future_move.append(Rotation.Anticlockwise)
                        dif = board.falling.left-1
                        for i in range(dif):
                            self.future_move.append(Direction.Left)
                    if board.next.shape == Shape.L:
                        self.next_piece_L=1

                elif self.T_tracker ==1:
                    self.T_tracker=0
                    moves.append(Rotation.Clockwise)
                    dif = 9-board.falling.right
                    for i in range(dif):
                        moves.append(Direction.Right)
                    if board.next.shape == Shape.Z:
                        self.next_piece_Z=1
                        self.future_move.append(Rotation.Clockwise)
                        dif = 8-board.falling.right
                        for i in range(dif):
                            self.future_move.append(Direction.Right)
            elif board.falling.shape==Shape.J:
                    dif = board.falling.left-2
                    # if(self.next_piece_J==1):
                    #     moves.extend([Rotation.Clockwise,Rotation.Clockwise])
                    # else:
                    moves.append(Rotation.Clockwise)
                    # if heightLeft > 20:
                    #     dif = dif - 1
                    for i in range(dif-1):
                        moves.append(Direction.Left)
            elif board.falling.shape==Shape.L:
                    dif = 7-board.falling.right
                    moves.append(Rotation.Anticlockwise)
                    # if heightLeft > 20:
                    #     dif = dif - 1
                    for i in range(dif-1):
                        moves.append(Direction.Right)
            elif board.falling.shape==Shape.S:
                dif = board.falling.left-1
                moves.append(Rotation.Anticlockwise)
                for i in range(dif):
                        moves.append(Direction.Left)
            elif board.falling.shape == Shape.O:
                if self.O_tracker==0:
                    self.O_tracker=1
                    dif = board.falling.left-4
                    for i in range(dif):
                            moves.append(Direction.Left)
                elif self.O_tracker==1:
                    self.O_tracker=0
                    dif = 8-board.falling.left
                    for i in range(dif):
                            moves.append(Direction.Right)
                if board.next.shape == Shape.J:
                    self.next_piece_J =1
                elif board.falling.shape==Shape.S:
                    dif = 8-board.falling.right
                    moves.append(Rotation.Clockwise)
                    for i in range(dif):
                            moves.append(Direction.Right)
                
                

                

            else:
                # if board.falling.shape == Shape.T:
                #     moves.extend([Rotation.Clockwise, Rotation.Clockwise])
                if board.falling.shape == Shape.L:
                    moves.append(Rotation.Clockwise)
                if board.falling.shape == Shape.J:
                    moves.append(Rotation.Anticlockwise)
                randNo = self.random.randint(0,3)
                if self.prev2 ==0:
                    self.prev2=1
                    dif = board.falling.left -2
                    for j in range(dif):
                        moves.append(Direction.Left)
                elif self.prev2 ==1:
                    self.prev2 =2
                    if board.falling.left >4:
                        dif = board.falling.left -4
                        for j in range(dif):
                            moves.append(Direction.Left)
                    elif board.falling.left<4:
                        dif = 4-board.falling.left
                        for j in range(dif):
                            moves.append(Direction.Right)
                elif self.prev2 ==2:
                    self.prev2 =0
                    dif = 6-board.falling.left
                    for j in range(dif):
                        moves.append(Direction.Right)
            moves.append(Direction.Drop)
            return moves




            #return self.possible_moves(board2)
            #rotations = [0,1,2,3]
            # height =0
            # for (x,y) in board.cells:
            #         if y > height:
            #             height = y
            # if (height<20):          
            #     self.moveBlock(board)
                
                
                # for i in range(10):       
                #     if i>board.falling.left:
                #         dif = i-board.falling.left
                #         for j in range(dif):
                #             yield Direction.Right
                #         print("left coordinate", board.falling.left)
                #         yield Direction.Drop
                #     elif i <board.falling.left:
                #         dif = board.falling.left-i
                #         #print("Difference: ",dif)
                #         for j in range(dif):
                #             yield Direction.Left
                #         print("left coordinate", board.falling.left)
                #         yield Direction.Drop
                #     else:
                #         yield Direction.Drop

                # a = self.random.randint(0,9)
                # move = []
                # if(board.falling.shape==Shape.I):
                #     return Rotation.Clockwise
                # if a>board.falling.left:
                #     #print(type(Shape.I))
                #     #print(type(board.falling.shape))
                #     #assert(board.falling.shape == board.falling.shape.I)
                
                #     #print(Shape.shape_to_cells)
                #     # print(board.falling.shape)
                    
                
                
                #     dif = a - board.falling.left
                #     for j in range(dif):
                #         move.append(Direction.Right)
                    
                #     # if board.falling.shape == Shape.I:
                #     #     yield Rotation.Clockwise
                #     # else: 
                #     #     return move
                # else:
                #     dif = board.falling.left - a
                #     for j in range(dif):
                #         move.append(Direction.Left)
                #     # if board.falling.shape == Shape.I:
                #     #     yield Rotation.Clockwise
                #     #     return move
                #     # else: 
                # return move
                


            

                # if board.falling.shape == Shape.I:
                #     if self.prev ==0:
                #         self.prev =1
                #         for i in range(board.falling.left):
                #             moves.append(Direction.Left)
                #     elif self.prev==1:
                #         self.prev = 0
                #         dif = 9-board.falling.left
                #         for i in range(dif):
                #             moves.append(Direction.Right)
                # elif board.falling.shape == Shape.O:
                #     if self.prev ==0:
                #         self.prev =1
                #         dif = board.falling.left -1
                #         for i in range(dif):
                #             moves.append(Direction.Left)
                #     elif self.prev==1:
                #         self.prev =0
                #         dif = 8-board.falling.left
                #         for i in range(dif):
                #             moves.append(Direction.Right)
                # elif board.falling.shape == Shape.T:
                #     if board.next.shape == Shape.L:
                #         if self.prev == 0:
                #             self.prev=1
                #             moves.append(Rotation.Anticlockwise)
                #             dif = board.falling.left -3
                #             for i in range(dif):
                #                 moves.append(Direction.Left)
                #         elif self.prev==1:
                #             self.prev =0
                #             moves.append(Rotation.Clockwise)
                #             dif = board.falling.left-3
                #         for i in range(dif): 
                #             moves.append(Direction.Left)      

                # else:
                #     # if board.falling.shape == Shape.T:
                #     #     moves.extend([Rotation.Clockwise, Rotation.Clockwise])
                #     if board.falling.shape == Shape.L:
                #         moves.append(Rotation.Clockwise)
                #     if board.falling.shape == Shape.J:
                #         moves.append(Rotation.Anticlockwise)
                #     randNo = self.random.randint(0,3)
                #     if self.prev2 ==0:
                #         self.prev2=1
                #         dif = board.falling.left -1
                #         for j in range(dif):
                #             moves.append(Direction.Left)
                #     elif self.prev2 ==1:
                #         self.prev2 =2
                #         if board.falling.left >4:
                #             dif = board.falling.left -4
                #             for j in range(dif):
                #                 moves.append(Direction.Left)
                #         elif board.falling.left<4:
                #             dif = 4-board.falling.left
                #             for j in range(dif):
                #                 moves.append(Direction.Right)
                #     elif self.prev2 ==2:
                #         self.prev2 =0
                #         dif = 7-board.falling.left
                #         for j in range(dif):
                #             moves.append(Direction.Right)
                # moves.append(Direction.Drop)
                # print("next shape:", board.next.shape)


            #self.print_board(board)
            # time.sleep(0.5)
            # board2 = board.clone()
            # print(board2.falling.cells)
            # board2.move(Direction.Right)
            # print(board2.falling.cells)
            # board2.move(Rotation.Clockwise)
            # print(board2.falling.cells)
            # print(board.falling.shape)
            # print(board.falling.cells)
            # print("occupied cells: ",board.cells)
            # print("score", board.score)
            # print("board height",board.cells.height)

        
            
            
            # print(Block.move(board,right,board,count=1))
                
                
            # Delete possible moves function and integrate it into the choose action function 
            # Remember to clone board for each possible move tested 
            #for all moves 
                # for all rotations
                        # clone
                        #move 
                        #score
                        #identify best move 
            #make best move
            
       



        # if self.random.random() > 0.97:
        #     # 3% chance we'll discard or drop a bomb
        #     return self.random.choice([
        #         Action.Discard,
        #         Action.Bomb,
        #     ])
        # else:
        #     # 97% chance we'll make a normal move
        #     return self.random.choice([
        #         Direction.Left,
        #         Direction.Right,
        #         Direction.Down,
        #         Rotation.Anticlockwise,
        #         Rotation.Clockwise,
        #     ])


SelectedPlayer = Player1

