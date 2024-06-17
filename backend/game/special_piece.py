from typing import Literal
from .piece import *
from backend.tools.exception import *

'''
(1)
you may be confused about the meaning of "user_z" and "nz" in the code below.

"user_z" is the user's piece's logic role, which is 0 for red, 1 for black, and 2 for gold.

"nz" is the piece's actual positon on the whole board, which is 0 for red, 1 for black, and 2 for gold.

(2)
and you may want to know why these class are all seemed to be empty.

these classes are just the name class for all pieces, and they don't have any specific rule.

the rule of each piece is defined in the frontend, and the backend only need to broadcast the move to all players.

of course, if you want to implement the rule of each piece, you can create a new class for each piece, and implement the rule in the class.

this can avoid players from cheating.
'''


class Soilder(Piece):
    '''
    Descriptions: Soilder piece 兵或卒
    '''
    def __init__(self, user_z: Literal[0,1,2], px: int, py: int):
        super().__init__(user_z, px, py)
        self.name = "Soilder"

    def _rule(self, nx: int, ny: int, nz: Literal[0,1,2])->bool:
        # 1. 不可以越过棋盘边界
        if nx < 0 or nx >= self.max_row or ny < 0 or ny >= self.max_col:
            raise OutOfBoardError("越界")
        # 2. 能且仅能移动一步
        if (abs(nx-self.px)+abs(ny-self.py)!= 1 and self.pz == nz) or (self.pz!=nz and not (self.py == 4 and ny==4 and self.px + nx == self.max_row-1)):
            raise InvalidMoveError("非法移动")
        # 3. 不可以后退
        if (nz==self.user_z and ny <= self.py) or( nz != self.user_z and ny > self.py):
            raise InvalidMoveError("不可以后退")
        return True

class WarHorse(Piece):
    '''
    Descriptions: WarHorse piece 马
    '''
    def __init__(self, user_z: Literal[0,1,2], px: int, py: int):
        super().__init__(user_z, px, py)
        self.name = "WarHorse"
    pass

class Chariot(Piece):

    '''
    Descriptions: Chariot piece 车
    '''
    def __init__(self, user_z: Literal[0,1,2], px: int, py: int):
        super().__init__(user_z, px, py)
        self.name = "Chariot"
    pass


class Gun(Piece):

    '''
    Descriptions: Gun piece 炮
    '''
    def __init__(self, user_z: Literal[0,1,2], px: int, py: int):
        super().__init__(user_z, px, py)
        self.name = "Gun"
    pass

class Leader(Piece):

    '''
    Descriptions: Leader piece 帅或将或王
    '''
    def __init__(self, user_z: Literal[0,1,2], px: int, py: int):
        super().__init__(user_z, px, py)
        self.name = "Leader"
    pass

class Advisor(Piece):

    '''
    Descriptions: Advisors piece 仕
    '''
    def __init__(self, user_z: Literal[0,1,2], px: int, py: int):
        super().__init__(user_z, px, py)
        self.name = "Advisor"
    pass


class Bishop(Piece):

    '''
    Descriptions: Bishop piece 象或相
    '''
    def __init__(self, user_z: Literal[0,1,2], px: int, py: int):
        super().__init__(user_z, px, py)
        self.name = "Bishop"
    pass
