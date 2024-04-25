import sys
import os
from dotenv import load_dotenv

load_dotenv()
import hashlib
from .piece import Piece
from .special_piece import *
from backend.message import *
from backend.log_tool import setupLogger

logger = setupLogger()

class GameTable:
    def __init__(self, user1: str, user2: str, user3: str):
        self.game_id = hashlib.md5(str(user1+user2+user3).encode('utf-8')).hexdigest()
        self.user1 = {'user_id':user1,'index':0} # 0
        self.user2 = {'user_id':user2,'index':1} # 1
        self.user3 = {'user_id':user3,'index':2} # 2

        self.Pieces:list[list[Piece]] = [[],[],[]]

        self.max_row = 9
        self.max_col = 5

        for i in range(3):
            self._initChess(i)

    def _initChess(self, user_z: int):
        # 初始化棋子
        # 1 King 2 Mardrain 2 Minister 2 Knight 2 Chariot 2 Cannon 5 Pawn
        self.Pieces[user_z].append(King(user_z, 4, 0))
        self.Pieces[user_z].append(Mardarin(user_z, 3, 0))
        self.Pieces[user_z].append(Mardarin(user_z, 5, 0))
        self.Pieces[user_z].append(Minister(user_z, 2, 0))
        self.Pieces[user_z].append(Minister(user_z, 6, 0))
        self.Pieces[user_z].append(Horse(user_z, 1, 0))
        self.Pieces[user_z].append(Horse(user_z, 7, 0))
        self.Pieces[user_z].append(Chariot(user_z, 0, 0))
        self.Pieces[user_z].append(Chariot(user_z, 8, 0))
        self.Pieces[user_z].append(Cannon(user_z, 1, 2))
        self.Pieces[user_z].append(Cannon(user_z, 7, 2))
        for i in range(self.max_row//2):
            self.Pieces[user_z].append(Pawn(user_z, 2*i, 3))

    def _getUserIndex(self, user:str) -> int:
        '''
        Description: 获取用户的索引
        Args:
            user: 用户名
        Returns:
            int: 用户的索引
        '''
        for item in [self.user1, self.user2, self.user3]:
            if item['user_id'] == user:
                return item['index']
        
    def searchGameTable(self, user:str) -> bool:
        '''
        检查用户是否在游戏中
        Args:
            user: 用户名
        Returns:
            bool: 是否在游戏中
        '''
        for item in [self.user1, self.user2, self.user3]:
            if item['user_id'] == user:
                return True
        else:
            return False

    def movePiece(self, user:str ,px: int, py: int, pz: int, nx: int, ny: int, nz: int):
        '''
        Description: 移动棋子
        Args:
            user: 用户名
            px: 原位置的行
            py: 原位置的列
            pz: 原位置的棋盘
            nx: 目标位置的行
            ny: 目标位置的列
            nz: 目标位置的棋盘
        Returns:
            bool: 是否移动成功
        '''
        if  user not in [self.user1['user_id'], self.user2['user_id'], self.user3['user_id']]:
            return NOT_JOIN_GAME # 用户不在游戏中
        try:
            user_z = self._getUserIndex(user) # 获取用户的索引
            for piece in self.Pieces[user_z]: # 遍历用户的所有棋子
                if piece.findPiece(px, py, pz): 
                    if piece.move(nx, ny, nz): # 移动棋子
                        logger.info(f"用户{user}移动棋子{piece.name}从({px},{py},{pz})到({nx},{ny},{nz})")
                        return SUCCESS
            else:
                return MOVE_NO_PIECE # 棋子不存在
        except InvalidMoveError:
            logger.error(f"棋子{piece.name}非法移动") #在这里统一打印日志
            return MOVE_INVALID # 非法移动
        except OutOfBoardError:
            logger.error(f"棋子{piece.name}越界")
            return MOVE_OUT_OF_BOARD # 越界
        except Exception as e:
            logger.error(e)
            return OTHER_ERROR # 其他错误
        

def fetchGameByUserID(user_id:str, game_tables:list[GameTable]) -> GameTable:
    '''
    Description: 根据用户ID获取游戏
    Args:
        user_id: 用户ID
    Returns:
        GameTable: 游戏
    '''
    for game_table in game_tables:
        if user_id in [game_table.user1['user_id'], game_table.user2['user_id'], game_table.user3['user_id']]:
            return game_table
    else:
        return None

