import numpy as np

WATER = " "
BOAT = "#"
HIT = "@"
MISS = "_"
SELECT = "*"

class Piece:
    def __init__(self) -> None:
        self.piece = None
        self.top = None
        self.right = None
        self.left = None
        self.bottom = None

        self.rotation = {}
        self.rotation_idx = 0
        self.length = None
        self.width = None
        # self.set_piece(self.rotation_idx)

    def L_shape(self):
        self.top = np.array([[WATER,BOAT],[WATER,BOAT],[BOAT,BOAT]])
        self.right = np.array([[BOAT,BOAT,BOAT],[WATER, WATER,BOAT]])
        self.left = np.array([[BOAT,WATER,WATER],[BOAT,BOAT,BOAT]])
        self.bottom = np.array([[BOAT,BOAT],[BOAT,WATER],[BOAT,WATER]])
        self.set_piece(self.rotation_idx)
    
    def I_shape(self):
        self.top = np.array([[BOAT],[BOAT],[BOAT],[BOAT]])
        self.right = np.array([[BOAT,BOAT,BOAT,BOAT]])
        self.left = np.array([[BOAT,BOAT,BOAT,BOAT]])
        self.bottom = np.array([[BOAT],[BOAT],[BOAT],[BOAT]])
        self.set_piece(self.rotation_idx)

    def Big_shape(self):
        self.top = np.array([[WATER,BOAT],[BOAT,BOAT],[WATER,BOAT],[BOAT,BOAT],[WATER,BOAT]])
        self.right = np.array([[WATER,BOAT,WATER,BOAT,WATER],[BOAT,BOAT,BOAT,BOAT,BOAT]])
        self.left = np.array([[BOAT,BOAT,BOAT,BOAT,BOAT],[WATER,BOAT,WATER,BOAT,WATER]])
        self.bottom = np.array([[BOAT,WATER],[BOAT,BOAT],[BOAT,WATER],[BOAT,BOAT],[BOAT,WATER]])
        self.set_piece(self.rotation_idx)

    def rotate_piece(self):
        if(self.rotation_idx < (len(self.rotations) - 1)):
            self.rotation_idx += 1
        else:
            self.rotation_idx = 0
        self.set_piece(self.rotation_idx)


    def set_piece(self, idx: int):
        self.rotation = {
            "top": self.top, 
            "left" : self.left,
            "bottom" : self.bottom, 
            "right" : self.right
            }
        self.rotations = list(self.rotation.keys())
        self.piece = self.rotation[self.rotations[idx]]
        self.length, self.width = self.piece.shape


class Board:
    def __init__(self):
        self.WIDTH = 8
        self.LENGTH = 8
        self.gameBoard = np.full(((self.WIDTH, self.LENGTH)), WATER)
        self.gameBoardHighlighted = np.full(((self.WIDTH, self.LENGTH)), WATER)

        # [[x. x. x. x. x. x. x. x.]
        # [y. 0. 0. 0. 0. 0. 0. 0.]
        # [y. 0. 0. 0. 0. 0. 0. 0.]
        # [y. 0. 0. 0. 0. 0. 0. 0.]
        # [y. 0. 0. 0. 0. 0. 0. 0.]
        # [y. 0. 0. 0. 0. 0. 0. 0.]
        # [y. 0. 0. 0. 0. 0. 0. 0.]
        # [y. 0. 0. 0. 0. 0. 0. 0.]]

    def add_piece(self, startPosX: int, startPosY: int, piece: Piece):
        for x_offset, x in enumerate(piece.piece):
            for y_offset, y in enumerate(x):
                self.gameBoard[(startPosY + x_offset),(startPosX + y_offset)] = y

    
    def is_valid_placement(self,  startPosX: int, startPosY: int, piece: Piece) -> bool:
        if(((piece.width + startPosX ) >= self.WIDTH ) or ((piece.length + startPosY) >= self.LENGTH)):
            print("Invalid placement | Outside of Board")
            return False
        else:
            for x_offset, x in enumerate(piece.piece):
                for y_offset, y in enumerate(x):
                    if self.gameBoard[(startPosY + x_offset),(startPosX + y_offset)] == WATER:
                        pass
                    else:
                        print("Invalid placement | Overlapping pieces ") 
                        return False
        
        return True

    def highlight(self, InputX, InputY):
        self.gameBoardHighlighted = self.gameBoard.copy()
        if InputY == None:
            for indexY, Row in enumerate(self.gameBoard):
                if self.gameBoardHighlighted[indexY, InputX] != HIT:
                    self.gameBoardHighlighted[indexY, InputX] = SELECT
            # for index, cell in enumerate(self.gameBoard[InputX]):
            #     self.gameBoardHighlighted[InputX, index] = SELECT
        else:
            self.gameBoardHighlighted[InputY, InputX] = SELECT
    
    def print(self,):
        out = "  A B C D E F G H\n"
        out += "  0 1 2 3 4 5 6 7\n"
        for line_num, x in enumerate(self.gameBoard):
                out += str(line_num) + " "
                for y in x:
                    if y == BOAT:
                        y = WATER
                    out += y + " " 
                out +=  str(line_num) + "\n"
        out += "  0 1 2 3 4 5 6 7\n"
        return out
    
    def printHighlated(self):
        out = "  A B C D E F G H\n"
        out += "  0 1 2 3 4 5 6 7\n"
        for line_num, x in enumerate(self.gameBoardHighlighted):
                out += str(line_num) + " "
                for y in x:
                    if y == BOAT:
                        y = WATER
                    out += y + " " 
                out +=  str(line_num) + "\n"
        out += "  0 1 2 3 4 5 6 7\n"
        return out
        

class GameState():
    def __init__(self) -> None:
        self.userInputX = None
        self.userInputY = None
        self.blocsRemaining = 0
        self.numOfMove = 0
        self.showHighlated = False

    def IncrementMoves(self):
        self.numOfMove += 1



class Game():
    def __init__(self) -> None:
        pass
        self.startingPieces = []
        self.board = Board()
        self.numOfActiveBoats = 0
    
    def setup(self):

        piece : Piece = Piece()
        piece.L_shape()
        self.startingPieces.append(piece)
        
        piece : Piece = Piece()
        piece.Big_shape()
        self.startingPieces.append(piece)

        piece : Piece = Piece()
        piece.I_shape()
        self.startingPieces.append(piece)

        piece : Piece = Piece()
        piece.L_shape()
        self.startingPieces.append(piece)

    def placePieces(self):
        for piece in self.startingPieces:
            placed = False
            rotated = False
            while placed is False:
                print(self.board.print())
                print(piece.piece)
                
                while rotated is False:
                    userInputRotate = input("Rotate? Y\\N? ")
                    userInputRotate = userInputRotate.lower()

                    if userInputRotate == "n":
                        rotated = True
                    elif userInputRotate == "y":
                        pass
                        piece.rotate_piece()
                        print(piece.piece)
                    else:
                        print("wrong input use Y\\N")

                userInputX = int(input(f"X coordinate " ))
                userInputY = int(input(f"Y coordinate " ))
                if self.board.is_valid_placement(userInputX, userInputY, piece):
                    self.board.add_piece(userInputX, userInputY, piece)
                    placed = True

    def autoPlacePieces(self):
        piece = self.startingPieces[0]
        piece.rotate_piece()
        piece.rotate_piece()
        self.board.add_piece(0, 0, piece)

        piece = self.startingPieces[1]
        piece.rotate_piece()
        piece.rotate_piece()
        piece.rotate_piece()
        self.board.add_piece(0, 4, piece)

        piece = self.startingPieces[2]
        self.board.add_piece(5, 0, piece)
    
    def shoot(self, InputX, InputY):
        print(f"num of active boats: {self.numOfActiveBoats}")
        print(self.board.print())
        print("please shoot")
        userInputX = InputX
        userInputY = InputY
        if userInputX > self.board.WIDTH or userInputY > self.board.LENGTH:
            print("outside of the board")
            return None
        if self.board.gameBoard[userInputY, userInputX] == BOAT or self.board.gameBoard[userInputY, userInputX] == HIT :
            self.board.gameBoard[userInputY, userInputX] = HIT
        else:
            self.board.gameBoard[userInputY, userInputX] = MISS

    

    def gameLoop(self):
        pass
        self.numOfActiveBoats = self.getActiveBoats()       
        if self.numOfActiveBoats <= 0: 
            exit()    

    
    def getActiveBoats(self):
        numOfActiveBoats = 0
        for x in self.board.gameBoard:
            for y in x:
                if y == BOAT:
                    numOfActiveBoats += 1
        return numOfActiveBoats

       
if __name__ == "__main__":  
    game = Game()
    game.setup()
    game.autoPlacePieces()
    print(game.board.gameBoard)
    game.gameLoop()
    print("Win")

