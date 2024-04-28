from typing import Literal

class Piece:
    def __init__(self, user_z: Literal[0,1,2], px: int, py: int):
        assert px >= 0 and px < 9 and py >= 0 and py < 5 and user_z >= 0 and user_z < 3
        self.user_z = user_z
        self.live = True
        self.px = px
        self.py = py
        self.pz = user_z

        self.name = 'Piece'

        self.max_row = 9
        self.max_col = 5

    def _rule(self, nx: int, ny: int, nz: Literal[0,1,2])->bool:
        '''
        Descriptions: Rules of piece movement
        '''
        return True

    def move(self, nx: int, ny: int, nz: Literal[0,1,2])->bool:
        '''
        Descriptions: Move piece to new position
        Parameters:
            nx, ny, nz: new position
        '''
        if self._rule(nx, ny, nz):
            self.px = nx
            self.py = ny
            self.pz = nz
            return True
        else:
            return False

    def setDead(self):
        '''
        Descriptions: Set piece as dead
        '''
        self.live = False

    def findPiece(self, px: int, py: int, pz: Literal[0,1,2])->bool:  
        '''
        Descriptions: Find piece by position
        Parameters:
            px, py, pz: position
        '''
        if self.live and self.px == px and self.py == py and self.pz == pz: 
            return True
        else:
            return False







