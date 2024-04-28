from typing import Literal
from .piece import *
from .exception import *

class Pawn(Piece):
    '''
    Descriptions: Pawn piece 兵或卒
    '''
    def __init__(self, user_z: Literal[0,1,2], px: int, py: int):
        super().__init__(user_z, px, py)
        self.name = "Pawn-"+('left' if px < self.max_row//2 else 'right')

    def _rule(self, nx: int, ny: int, nz: Literal[0,1,2])->bool:
        # 1. 不可以越过棋盘边界
        if nx < 0 or nx >= self.max_row or ny < 0 or ny >= self.max_col:
            raise OutOfBoardError("越界")
        # 2. 能且仅能移动一步
        if abs(nx-self.px)+abs(ny-self.py)!= 1:
            raise InvalidMoveError("非法移动")
        # 3. 不可以后退
        if (nz==self.user_z and ny < self.py) or ny > self.py:
            raise InvalidMoveError("不可以后退")
        return True

class Horse(Piece):
    def __init__(self, user_z: Literal[0,1,2], px: int, py: int):
        super().__init__(user_z, px, py)
    '''
    Descriptions: Horse piece 马
    '''
    pass

class Chariot(Piece):
    def __init__(self, user_z: Literal[0,1,2], px: int, py: int):
        super().__init__(user_z, px, py)
    '''
    Descriptions: Chariot piece 车
    '''
    pass


class Cannon(Piece):
    def __init__(self, user_z: Literal[0,1,2], px: int, py: int):
        super().__init__(user_z, px, py)
    '''
    Descriptions: Cannon piece 炮
    '''
    pass

class King(Piece):
    def __init__(self, user_z: Literal[0,1,2], px: int, py: int):
        super().__init__(user_z, px, py)
    '''
    Descriptions: King piece 帅或将或王
    '''
    pass

class Mardarin(Piece):
    def __init__(self, user_z: Literal[0,1,2], px: int, py: int):
        super().__init__(user_z, px, py)
    '''
    Descriptions: Mardarins piece 仕
    '''
    pass


class Minister(Piece):
    def __init__(self, user_z: Literal[0,1,2], px: int, py: int):
        super().__init__(user_z, px, py)
    '''
    Descriptions: Minister piece 象或相
    '''
    pass
