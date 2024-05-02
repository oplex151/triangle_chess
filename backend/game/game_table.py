import sys
import os
from flask import Flask, request, jsonify
from typing import Tuple, Union
from dotenv import load_dotenv

load_dotenv()
import hashlib
import random
from .piece import Piece
from .special_piece import *
from backend.message import *
from backend.tools import setupLogger

logger = setupLogger()

class GameTable:
    def __init__(self,users:list[int]):
        self.game_id = hashlib.md5(str(sum(users)).encode('utf-8')).hexdigest()
        self.user1 = {'user_id':users[0],'index':0} # 0
        self.user2 = {'user_id':users[1],'index':1} # 1
        self.user3 = {'user_id':users[2],'index':2} # 2

        self.Pieces:list[list[Piece]] = [[],[],[]]
        
        self.turn = 0 # 目前轮到谁
        self.game_state = "ongoing"  # 游戏状态：ongoing（进行中）、win（胜利）、draw（平局）
        self.winner = -1 # 无胜者为-1

        self.max_row = 9
        self.max_col = 5

        for i in range(3):
            self._initChess(i)

    def _initChess(self, user_z: int):
        # 初始化棋子
        # 1 King 2 Mardrain 2 Minister 2 Knight 2 Chariot 2 Cannon 5 Pawn
        # 说明：x是棋盘的横轴，y是棋盘的纵轴，z是用户索引
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
        for i in range(self.max_row//2+1):
            self.Pieces[user_z].append(Pawn(user_z, 2*i, 3))

    def _getUserIndex(self, user:int) -> int:
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
        
    def searchGameTable(self, userid:int) -> bool:
        '''
        检查用户是否在游戏中
        Args:
            user: 用户名
        Returns:
            bool: 是否在游戏中
        '''
        for item in [self.user1, self.user2, self.user3]:
            if item['user_id'] == userid:
                return True
        else:
            return False

    def movePiece(self, user:int ,px: int, py: int, pz: int, nx: int, ny: int, nz: int):
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
            logger.error(f"用户{user}不在游戏中")
            return NOT_JOIN_GAME # 用户不在游戏中

        if self._getUserIndex(user) != self.turn:
            logger.error(f"用户{user}不是轮到移动棋子")
            return NOT_YOUR_TURN # 不是轮到该用户移动棋子
        try:
            user_z = self._getUserIndex(user) # 获取用户的索引
            for piece in self.Pieces[user_z]: # 遍历用户的所有棋子
                if piece.findPiece(px, py, pz): 
                    kill_piece = self.isWithPiece(nx, ny, nz) # 获取被杀死的棋子
                    if piece.move(nx, ny, nz): # 移动棋子
                        logger.info(f"用户{user}移动棋子{piece.name}从({px},{py},{pz})到({nx},{ny},{nz})")
                        # 判断是否杀死棋子
                        if kill_piece:
                            logger.info(f"用户{user}击杀棋子{kill_piece.name}({nx},{ny},{nz}) by {piece.name}({px},{py},{pz})")
                            kill_piece.setDead() # 被杀死的棋子死亡
                            # 如果死的是某个人的
                        # print(piece.name, piece.live)
                        # print(kill_piece.name, kill_piece.live)
                        # 判断游戏是否结束
                        if self.checkGameEnd():
                            return GAME_END
                        
                        self.turn = (self.turn+1)%3 # 切换到下一个用户

                        return SUCCESS
            else:
                logger.error(f"用户{user}没有棋子在({px},{py},{pz})")
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
        
    def isWithPiece(self, px: int, py: int, pz: int) -> Piece:
        '''
        Description: 判断某一位置是否有棋子
        Args:
            px: 位置的行
            py: 位置的列
            pz: 位置的棋盘
        Returns:
            Piece: 存在的棋子 
        '''
        for user_z in range(3):
            for i,piece in enumerate(self.Pieces[user_z]):
                if piece.findPiece(px, py, pz):
                    return piece
        else:
            return None
    
    def checkGameEnd(self):
        # 检查胜利条件和平局条件
        if self.checkVictory():
            self.game_state = "win"
            return True
        
        if self.checkDraw():
            self.game_state = "draw"
            return True
        
        return False

    def checkVictory(self):
        # 实现判断胜利条件的逻辑
        # 计算存活的 King 的数量
        living_kings = [user_z for user_z in range(3) if self.Pieces[user_z][0].live]
        if len(living_kings) == 1:
            # 只有一个 King 存活，游戏结束
            self.winner = living_kings[0]
            return True
        
        return False
    
    def checkDraw(self):
        # 实现判断平局条件的逻辑
        pass

    def showBoard(self):
        '''
        Description: 展示棋盘
        '''
        board = ''
        for user_z in range(3):
            board += f"第{user_z+1}位玩家:\n"
            for i in list(range(self.max_col))[::-1]:
                for j in range(self.max_row):
                    piece = self.isWithPiece(j, i, user_z)
                    if piece and piece.live:
                        # 填充为宽12的字符串
                        board += piece.name.center(12) + '|'
                    else:
                        board += ' '*12+ '|'
                board += '\n'
        print(board)


class RoomManager:
    def __init__(self, users: Union[list[int], int]):
        # 随机生成一串字符串
        self.room_id:str = hashlib.md5(str(random.randint(0,1000000000)).encode('utf-8')).hexdigest()
        self.users = None
        self.game_table = None

        if isinstance(users, list):
            self.users = users
        else:
            self.users = [users]

        self.holder = self.users[0] # 房主
    
    def getRoomId(self) -> str:
        return self.room_id
    
    def addGameTable(self, game_table: GameTable):
        self.game_table = game_table

    def addUser(self, userid: Union[int, list[int]]):
        if isinstance(userid, list):
            for u in userid:
                if u not in self.users:
                    self.addUser(u)
        else:
            if userid not in self.users:
                self.users.append(userid)
        
    
    def removeUser(self, userid:int):
        if userid in self.users:
            self.users.remove(userid)
            logger.info(f"用户{userid}退出房间{self.room_id}")
            return True
        return False
    
    # def alertSide(self, user:str, new_sid:str):
    #     for i,(uid,sid) in enumerate(self.users):
    #         if uid == user:
    #             self.users[i][1] = new_sid
    #             return
        


# def fetchGameByUserID(user_id:str, game_tables:list[GameTable]) -> GameTable:
#     '''
#     Description: 根据用户ID获取游戏
#     Args:
#         user_id: 用户ID
#     Returns:
#         GameTable: 游戏
#     '''
#     for game_table in game_tables:
#         if user_id in [game_table.user1['user_id'], game_table.user2['user_id'], game_table.user3['user_id']]:
#             return game_table
#     else:
#         return None


def fetchRoomByRoomID(room_id:str, room_managers:list[RoomManager]) -> RoomManager:
    '''
    Description: 根据房间ID获取房间
    Args:
        room_id: 房间ID
    Returns:
        RoomManager: 房间
    '''
    for room in room_managers:   
        if room.getRoomId() == room_id:
            return room
    else:
        return None
    
def inWhitchRoom(user_id:int, room_managers:list[RoomManager]) -> str:
    '''
    Description: 判断用户是否在某个房间中
    Args:
        user_id: 用户ID
        room_managers: 房间列表
    Returns:
        str: 房间ID
    '''
    for room in room_managers:
        # for (uid,sid) in room.users:
        #     if uid == user_id:
        #         return room.getRoomId()
        if user_id in room.users:
            return room.getRoomId()
    else:
        return None
    
# def ifInRoomBySid(sid:str, room_managers:list[RoomManager]) :
#     '''
#     Description: 根据sid判断用户是否在某个房间中
#     Args:
#         sid: sid
#         room_managers: 房间列表
#     Returns:
#         str: 房间ID
#     '''
#     for room in room_managers:
#         for (uid,sid) in room.users:
#             if sid == sid:
#                 return room.getRoomId(),uid
#     else:
#         return None,None