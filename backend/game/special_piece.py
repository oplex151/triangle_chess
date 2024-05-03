from typing import Literal
from .piece import *
from .exception import *

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
        if abs(nx-self.px)+abs(ny-self.py)!= 1:
            raise InvalidMoveError("只能走一步")
        # 3. 不可以后退
        if (nz==self.user_z and ny < self.py) or ny > self.py:
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
