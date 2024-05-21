from enum import Enum
from typing import Dict, Union
from dotenv import load_dotenv

load_dotenv()
import hashlib
import random
import datetime
from .piece import Piece
from .special_piece import *
from .record import GameRecord
from backend.message import *
from backend.tools import setupLogger

logger = setupLogger()

class UserDict(Dict):
    userid:int
    username:str

class EnumGameState(Enum):
    ongoing = "ongoing"
    win = "win"
    draw = "draw"

class GameTable:
    max_row = 9
    max_col = 5
    def __init__(self,users:list[UserDict], viewers:list[UserDict] = []):
        self.game_id = hashlib.md5(str(sum([user['userid'] for user in users])).encode('utf-8')).hexdigest()
        self.users = users
        self.lives = [True,True,True]
        self.viewers = viewers

        self.Pieces:list[list[Piece]] = [[],[],[]]
        
        self.turn = 0 # 目前轮到谁
        self.game_state = EnumGameState.ongoing # 游戏状态：ongoing（进行中）、win（胜利）、draw（平局）
        self.winner = -1 # 无胜者为-1
        self.winner_id = -1
        self.step_count = 0

        self.draw_requester = None  # 发起求和请求的玩家
        self.draw_respondents = set()  # 记录回应求和请求的玩家
        self.draw_agree = set()  # 记录对求和请求的回应

        self.record = GameRecord(
                p1=self.users[0]['userid'],
                p2=self.users[1]['userid'],
                p3=self.users[2]['userid']
            )

        for i in range(3):
            self._initChess(i)

    def _initChess(self, user_z: int):
        # 初始化棋子
        # 1 Leader 2 Mardrain 2 Bishop 2 Knight 2 Chariot 2 Gun 5 Soilder
        # 说明：x是棋盘的横轴，y是棋盘的纵轴，z是用户索引
        self.Pieces[user_z].append(Leader(user_z, 4, 0))
        self.Pieces[user_z].append(Advisor(user_z, 3, 0))
        self.Pieces[user_z].append(Advisor(user_z, 5, 0))
        self.Pieces[user_z].append(Bishop(user_z, 2, 0))
        self.Pieces[user_z].append(Bishop(user_z, 6, 0))
        self.Pieces[user_z].append(WarHorse(user_z, 1, 0))
        self.Pieces[user_z].append(WarHorse(user_z, 7, 0))
        self.Pieces[user_z].append(Chariot(user_z, 0, 0))
        self.Pieces[user_z].append(Chariot(user_z, 8, 0))
        self.Pieces[user_z].append(Gun(user_z, 1, 2))
        self.Pieces[user_z].append(Gun(user_z, 7, 2))
        for i in range(self.max_row//2+1):
            self.Pieces[user_z].append(Soilder(user_z, 2*i, 3))

    def _getUserIndex(self, userid:int) -> int:
        '''
        Description: 获取用户的索引
        Args:
            userid: 用户id
        Returns:
            int: 用户的索引
        '''
        for index,item in enumerate(self.users):
            if item['userid'] == userid:
                return index
        else:
            raise ValueError("该用户不是玩家")
        
    def searchGameTable(self, userid:int) -> bool:
        '''
        检查用户是否在游戏中
        Args:
            user: 用户名
        Returns:
            bool: 是否在游戏中
        '''
        for item in self.users:
            if item['userid'] == userid:
                return True
        else:
            return False

    def movePiece(self, userid:int ,px: int, py: int, pz: int, nx: int, ny: int, nz: int):
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
        if  userid not in [u['userid'] for u in self.users]:
            logger.error(f"用户{userid}不在游戏中")
            return NOT_JOIN_GAME # 用户不在游戏中

        if self._getUserIndex(userid) != self.turn:
            logger.error(f"当前没有用户{userid}轮到移动棋子，应该是{self.turn}号玩家")
            return NOT_YOUR_TURN # 不是轮到该用户移动棋子
        try:
            user_z = self._getUserIndex(userid) # 获取用户的索引
            for piece in self.Pieces[user_z]: # 遍历用户的所有棋子
                if piece.findPiece(px, py, pz): 
                    # 获取将要被杀死的棋子
                    kill_piece = self.isWithPiece(nx, ny, nz) 
                    # 移动棋子
                    if kill_piece and kill_piece.user_z == user_z:
                        # 不能杀自己的棋子
                        return MOVE_INVALID
                    if piece.move(nx, ny, nz):
                        logger.info(f"用户{userid}移动棋子{piece.name}从({px},{py},{pz})到({nx},{ny},{nz})")
                        # 判断是否杀死棋子
                        if kill_piece:
                            logger.info(f"用户{userid}击杀棋子{kill_piece.name}({nx},{ny},{nz}) by {piece.name}({px},{py},{pz})")
                            # 被杀死的棋子死亡
                            kill_piece.setDead() 
                            # 杀死Leader，该玩家阵亡，请前端自己判断阵亡，后端不发出通知
                            if kill_piece.name == 'Leader':
                                self.lives[kill_piece.user_z] = False
                                logger.info(f"用户{kill_piece.user_z}阵亡")

                        # 记录弈子移动
                        self.step_count += 1

                        # 记录这一步
                        chessType = "piece"
                        startPos = str(px) + ',' + str(py) + ',' + str(pz)
                        endPos = str(nx) + ',' + str(ny) + ',' + str(nz)
                        self.record.recordMove(userid, chessType, startPos, endPos)

                        # 判断游戏是否结束
                        if self.checkGameEnd():
                            return GAME_END

                        self.turnChange() # 切换到下一个玩家

                        return SUCCESS
            else:
                logger.error(f"用户{userid}没有棋子在({px},{py},{pz})")
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

    def addViewer(self, user:UserDict):
        '''
        Description: 添加观战者
        Args:
            user: 用户
        Returns:
            bool: 是否添加成功
        '''
        if user['userid'] in [u['userid'] for u in self.users]:
            return False
        else:
            self.viewers.append(user)

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
    
    def turnChange(self):
        index = 0
        self.turn = (self.turn+1)%3
        while not self.lives[self.turn]:
            self.turn = (self.turn+1)%3
            index += 1
            if index > 3:
                return

    def getAlivePlayers(self):
        '''
        Description: 返回存活玩家的 userid 列表。
        Returns:
            alive_players: 存活玩家的列表
        '''
        # 存活玩家的列表
        alive_players = []
        
        # 遍历 lives 列表中的存活状态
        for index, alive in enumerate(self.lives):
            if alive:
                alive_players.append(self.users[index]['userid'])
        
        # 返回存活玩家的 userid 列表
        return alive_players

    def surrender(self, userid:int)->int:
        '''
        Description: 处理投降请求
        '''
        # 将投降的玩家设为死亡
        for index,item in enumerate(self.users):
            if item['userid'] == userid:
                self.lives[index] = False
                if self.turn == self._getUserIndex(userid):
                    # 投降玩家，切换到下一个玩家
                    self.turnChange()
        if self.checkGameEnd():
            return GAME_END
        else:   
            return SUCCESS

    def requestDraw(self, userid:int):
        '''
        Description: 处理求和请求
        '''
        # 如果已经有一个求和请求，则忽略新请求
        if self.draw_requester is not None:
            return
        
        # 记录发起求和请求的玩家
        self.draw_requester = userid
        
        # 初始化回应求和请求的玩家列表
        self.draw_respondents = set()

    def respondDraw(self, userid:int, agree:bool):
        '''
        Description: 处理求和回应
        '''
        # 如果用户不是求和请求的回应对象之一，忽略
        if self.draw_requester is None or userid == self.draw_requester or self.lives[userid] == False:
            return
        
        # 添加回应的用户
        self.draw_respondents.add(userid)
        
        # 添加对求和请求的回应
        self.draw_agree.add(agree)

    def setDraw(self, agree:bool):
        '''
        Description: 处理求和的结果
        '''
        if agree:
            # 所有玩家都同意求和
            self.game_state = EnumGameState.draw
        else:
            # 至少有一个玩家不同意求和
            self.draw_requester = None
            self.draw_respondents = set()

    def checkGameEnd(self):
        # 检查胜利条件和平局条件
        if self.checkVictory():
            self.game_state = EnumGameState.win
            return True
        
        if self.checkDraw():
            self.game_state = EnumGameState.draw
            return True
        
        return False

    def checkVictory(self):
        # 实现判断胜利条件的逻辑
        live_users = [index for index, live in enumerate(self.lives) if live]
        if len(live_users) == 1:
            # 只有一个 Leader 存活，游戏结束
            self.winner =live_users[0]
            self.winner_id = self.users[self.winner]['userid'] if self.winner != -1 else -1
            return True
        return False
    
    def checkDraw(self):
        # 实现判断平局条件的逻辑
        pass

    def getGameInfo(self):
        '''
        Description: 获取游戏数据
        Returns:
            dict: 游戏数据
        '''
        data ={
            'turn': self.turn,
            'game_state': self.game_state.value,
            'winner': self.winner, # 胜利者的索引0,1,2,-1
            'lives': self.lives,
            'viewers': self.viewers,
            'users': self.users,
            'pieces': [piece.getPieceInfo() for piece_list in self.Pieces for piece in piece_list]
        }
        return data

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

class RoomType(Enum):
    created = 'created'
    matched ='matched'

class RoomManager:
    def __init__(self, users: Union[list[UserDict], UserDict], room_type: RoomType=RoomType.created):
        # 随机生成一串字符串
        self.room_id:str = hashlib.md5(str(random.randint(0,1000000000)).encode('utf-8')).hexdigest()
        self.users:list[UserDict] | UserDict = None
        self.game_table = None

        if isinstance(users, list):
            self.users = users
        else:
            self.users = [users]

        self.holder = self.users[0]# 房主
        self.room_type = room_type # 房间类型
    
    def getRoomId(self) -> str:
        return self.room_id
    
    def addGameTable(self, game_table: GameTable):
        self.game_table = game_table

    def removeGameTable(self):
        self.game_table = None

    def addUser(self, user: Union[UserDict, list[UserDict]]):
        if isinstance(user, list):
            for u in user:
                if u not in self.users:
                    self.addUser(u)
        else:
            if user not in self.users:
                self.users.append(user)
        
    
    def removeUser(self, userid:int, force=False):
        for user in self.users:
            if user['userid'] == userid:
                leaved_user = user
                logger.info(f"User {userid} leave room {self.room_id}"+f"this room's users: {self.users}")
                self.users.remove(leaved_user)
                if self.holder['userid'] == leaved_user['userid'] and len(self.users) > 0:
                    # 房主退出房间，更换房主
                    self.holder = self.users[0]
                if self.game_table and leaved_user['userid'] in [u['userid'] for u in self.game_table.viewers]:
                    # 观战者离开直接送出游戏
                    self.game_table.viewers.remove(leaved_user)
                elif force and self.game_table and leaved_user['userid'] in [u['userid'] for u in self.game_table.users]:
                    # 强制退出房间和游戏
                    self.game_table.users.remove(leaved_user)
                return True
        else:
            return False
            

    def getRoomInfo(self):
        '''
        Description: 获取房间信息
        Returns:
            dict: 房间信息
        '''
        data = {
            'room_id': self.room_id,
            'room_type': self.room_type.value,
            'holder': self.holder,
            'users': self.game_table.users if self.game_table else self.users[:3],
            'viewers': self.game_table.viewers if self.game_table else self.users[3:] if len(self.users) > 3 else [],
        }
        return data



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
    
def inWhitchRoom(userid:int, room_managers:list[RoomManager]) -> str:
    '''
    Description: 判断用户是否在某个房间中
    Args:
        userid: 用户ID
        room_managers: 房间列表
    Returns:
        str: 房间ID
    '''
    for room in room_managers:
        if userid in [user['userid'] for user in room.users]:
            return room.getRoomId()
    else:
        return None
