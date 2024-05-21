import os
import sys
from pathlib import Path
import threading
import time

project_root = Path(__file__).parent.parent.absolute()
os.environ['PROJECT_ROOT'] = str(project_root)
sys.path.append(str(Path(__file__).resolve().parent.parent))
print("Project root set to:", os.environ['PROJECT_ROOT']) # 设置项目根目录

import flask
from flask_socketio import SocketIO,join_room,leave_room,emit,close_room
from flask_cors import CORS
from flask import request,current_app
from backend.global_var import *
from backend.tools import setupLogger, getParams
from backend.user_manage import *
from backend.game.exception import *
from backend.game.record import *
from message import *
from backend.game import *

app = flask.Flask(__name__)
CORS(app,cors_allowed_origins="*")
socketio = SocketIO(app, cors_allowed_origins="*")

# 日志工具
logger = setupLogger()

@app.route('/api/login', methods=['POST'])
def loginApi():
    '''
    Args:
        username: 用户名
        password: 密码
    Returns:
        登录成功200
    '''
    params = {'username':str, 'password':str}
    try:
        username,password = getParams(params,request.form)
    except:
        return "{message: 'parameter error'}",PARAM_ERROR
    return login(username, password)

@app.route('/api/register', methods=['POST'])
def registerApi():
    '''
    Args:
        username: 用户名
        password: 密码
    Returns:
        注册成功200
    '''
    params = {'username':str, 'password':str}
    try:
        username,password = getParams(params,request.form)
    except:
        return "{message: 'parameter error'}",PARAM_ERROR
    return register(username, password)

@app.route('/api/logout', methods=['POST'])
def logoutApi():
    '''
    Args:
        userid: 用户id
    Returns:
        登出成功200
    '''
    params = {'userid':int}
    try:
        userid = getParams(params,request.form)
    except:
        return "{message: 'parameter error'}",PARAM_ERROR
    return logout(userid)

@socketio.on('connect')
def connect():
    '''
    建立socket连接
    '''
    logger.info("User {0} connect".format(request.sid))

@socketio.on('disconnect')
def disconnect():
    '''
    断开socket连接
    '''
    global rooms,sid2uid,sessions,match_queue,rank_queue
    if request.sid in sid2uid:
        # 断开连接时,判断用户是否在房间中,如果在房间中,则退出房间
        userid = sid2uid[request.sid]
        sid2uid.pop(request.sid) 
        try:
            room_id = inWhitchRoom(userid,rooms)
            if room_id is not None:
                room:RoomManager = fetchRoomByRoomID(room_id,rooms)
                if room is not None:
                    room.removeUser(userid)
                    leave_room(room_id)
                    if len(room.users) == 0:
                        rooms.remove(room)
                        close_room(room=room_id,namespace='/')
                        logger.info(f"Room {room_id} is empty, remove it")
                    else:
                        emit('leaveRoomSuccess',{'userid':userid,'username':sessions[userid],'room_info':room.getRoomInfo()},to=room.room_id,namespace='/')
        except:
            logger.error("User {0} disconnect, ".format(userid), exc_info=True)

        # 断开连接时,判断用户是否在匹配队列中,如果在匹配队列中,则移除 
        if match_queue.is_have(userid):
            logger.info(f"User {userid} leave match queue")
            match_queue.remove(userid)

        # 断开连接时,判断用户是否在排位队列中,如果在排位队列中,则移除
        if rank_queue.is_have(userid):
            logger.info(f"User {userid} leave rank queue")
            rank_queue.remove(userid)
        
    logger.info("User {0} disconnect".format(request.sid))

@socketio.event
def createRoom(data):
    '''
    Description: 创建房间
    Args:
        userid: 用户id 作为房主 int
    '''
    global rooms,sid2uid,sessions
    params = {'userid':int}
    try:
        userid = getParams(params,data)
    except:
        emit('processWrong',{'status':PARAM_ERROR},to=request.sid)
        return
    
    room_id = inWhitchRoom(userid,rooms)
    if room_id is not None:
        logger.error("User {0} is already in room {1}".format(userid,room_id))
        emit('processWrong',{'status':ALREADY_IN_ROOM},to=request.sid)
        return
    new_room = RoomManager(UserDict(userid=userid,username=sessions[userid]))
    rooms.append(new_room)
    room_id = rooms[-1].room_id
    room_type = rooms[-1].room_type
    join_room(room_id)
    logger.info(f"Create room {room_id} by user {userid}, type is {room_type}, sid={request.sid}\n"
                +f"this room's users: {new_room.users}")
    emit('createRoomSuccess',{'room_id':room_id,'room_info':new_room.getRoomInfo()},to=request.sid)
    # 更新sid2uid
    if request.sid not in sid2uid:
        sid2uid[request.sid] = userid

@socketio.event
def joinRoom(data):
    '''
    Description: 加入房间
    Args:
        room_id: 房间id  str
        userid: 用户id  int
    Return:
        成功返回200
        room_id: 房间id  str
        userid: 用户id  int
        username: 用户名 str
    '''
    global rooms,sessions,sid2uid
    parms = {'room_id':str, 'userid':int}
    try:
        room_id,userid = getParams(parms,data)
    except:
        logger.error("Join room error", exc_info=True)
        emit('processWrong',{'status':PARAM_ERROR},to=request.sid)
        return
    
    room = fetchRoomByRoomID(room_id,rooms)
    if room is None:
        emit('processWrong',{'status':ROOM_NOT_EXIST},to=request.sid)
        return
    # 查询该用户是否在某个房间中
    tmp_id = inWhitchRoom(userid,rooms)
    # 已经在某个房间中, 先退出
    if tmp_id is not None and tmp_id != room_id: 
        logger.info(f"User {userid} leave room {tmp_id}"+
                    f"this room's users: {fetchRoomByRoomID(tmp_id,rooms).users}")
        room = fetchRoomByRoomID(tmp_id,rooms)
        room.removeUser(userid, force=True)
        emit('leaveRoomSuccess',{'userid':userid,'username':sessions[userid],'room_info':room.getRoomInfo()},to=tmp_id)
        leave_room(tmp_id)
        room = fetchRoomByRoomID(room_id,rooms)
    # 已经在这个房间中, 不可以重复加入
    elif tmp_id is not None: 
        logger.info(f"User {userid} already in room {room_id}"+
                    f"this room's users: {fetchRoomByRoomID(room_id,rooms).users}")
        emit('processWrong',{'status':ALREADY_IN_ROOM},to=request.sid)
        return
    # 用户在游戏中
    elif room.game_table is not None and room.game_table.searchGameTable(userid): 
        logger.info(f"User {userid} rejoin to game {room.game_table.game_id}")
        emit('rejoinGameSuccess',{'room_id':room_id},to=request.sid,namespace='/')
    
    room.addUser(UserDict(userid=userid,username=sessions[userid]))
    join_room(room_id)
    logger.info(f"User {userid} join room {room_id}, sid={request.sid}"
                +f"this room's users: {room.users}")
    emit('joinRoomSuccess',{'room_id':room_id,'userid':userid,'username':sessions[userid],'room_info':room.getRoomInfo()},to=room_id)
    # 更新sid2uid
    if request.sid not in sid2uid: 
        sid2uid[request.sid] = userid

@socketio.event
def leaveRoom(data):
    '''
    Description: 离开房间
    Args:
        room_id: 房间id str
        userid: 用户id int
    '''
    global rooms,sid2uid,sessions
    parms = {'room_id':str, 'userid':int}
    try:
        room_id,userid = getParams(parms,data)
    except:
        logger.error("Leave room error", exc_info=True)
        emit('processWrong',{'status':PARAM_ERROR},to=request.sid)
        return
    room:RoomManager = fetchRoomByRoomID(room_id,rooms)
    if room is None:
        logger.error("No such room {0}".format(room_id))
        emit('processWrong',{'status':ROOM_NOT_EXIST},to=request.sid)
        return
    if room.removeUser(userid):
        emit('leaveRoomSuccess',{'userid':userid,'username':sessions[userid],'room_info':room.getRoomInfo()},to=room_id)
        leave_room(room_id)
        # 更新sid2uid
        if request.sid in sid2uid:
            sid2uid.pop(request.sid)
        # 房间为空, 移除房间
        if len(room.users) == 0:
            rooms.remove(room)
            close_room(room=room_id,namespace='/')
            logger.info(f"Room {room_id} is empty, remove it")
    else:
        logger.error("User {0} not in room {1}".format(userid,room_id))
        emit('processWrong',{'status':NOT_IN_ROOM},to=request.sid)

@app.route('/api/game/create', methods=['POST'])
def createGameApi():
    '''
    Args:
        userid: 用户id 房主 int
        room_id: 房间id str
    Returns:
        成功返回200
        game_id: 游戏id str
        users: 玩家列表 list
        usernames: 玩家用户名列表 list
    '''
    global rooms
    params = {'userid':int, 'room_id':str}
    try:
        userid,room_id = getParams(params,request.form) # TODO::检查房主是否存在
    except:
        return "{message: 'parameter error'}",PARAM_ERROR
    try:
        room = fetchRoomByRoomID(room_id,rooms)
        if room is None:
            emit('processWrong',{'status':ROOM_NOT_EXIST},to=uid2sid(userid),namespace='/')
            return "{message: '房间不存在！'}",ROOM_NOT_EXIST
        if len(room.users) < 3:
            emit('processWrong',{'status':ROOM_NOT_ENOUGH},to=uid2sid(userid),namespace='/')
            return "{message: '房间人数不足！'}",ROOM_NOT_ENOUGH

        game:GameTable = GameTable(room.users[:3], room.users[3:] if len(room.users) > 3 else [])
        
        room.addGameTable(game)
        
        emit('createGameSuccess',{'game_id':game.game_id,'room_info':room.getRoomInfo()},to=room_id,namespace='/')

        logger.info("Create game: {0}".format(game.game_id))
        return "{}",SUCCESS
    except Exception as e:
        logger.error("Create game error due to {0}".format(str(e)), exc_info=True)
        emit('processWrong',{'status':GAME_CREATE_FAILED},to=uid2sid(userid),namespace='/')
        return "{message: 'create game error'}",GAME_CREATE_FAILED

@app.route('/api/game/init', methods=['POST'])
def initGame():
    '''
    Description: 初始化游戏，前端主动请求
    Args:
        room_id: 房间id str
    Returns:
        成功返回200
        game_info: 游戏信息 dict
    '''
    global rooms
    params = {'room_id':str}
    try:
        room_id = getParams(params,request.form)
    except:
        return "{message: 'parameter error'}",PARAM_ERROR

    room:RoomManager = fetchRoomByRoomID(room_id,rooms)

    if room is None: return "{message: 'room not exist'}",ROOM_NOT_EXIST

    game:GameTable = room.game_table
 
    return jsonify({'game_info':game.getGameInfo()}),SUCCESS


@socketio.event
def movePiece(data):
    '''
    Args:
        userid: 用户id           int 
        x1: 起始横坐标           int
        y1: 起始纵坐标           int
        z1: 起始棋盘             int
        x2: 目标横坐标           int
        y2: 目标纵坐标           int
        z2: 目标棋盘             int
    Returns:
        移动成功200(房间广播)
        userid: 用户id           int
        status:状态码            int       
        x1: 起始横坐标           int
        y1: 起始纵坐标           int
        z1: 起始棋盘             int
        x2: 目标横坐标           int
        y2: 目标纵坐标           int
        z2: 目标棋盘             int
    ''' 
    global rooms,sessions
    params = {'userid':int,  'x1':int, 'y1':int, 'z1':int, 'x2':int, 'y2':int, 'z2':int}
    try:
        userid,x1,y1,z1,x2,y2,z2 = getParams(params,data)
    except ValueError as e:
        logger.error(e)
        emit('processWrong',{'status':PARAM_ERROR},to=request.sid)
        return
    # 先判断用户是否在房间中
    room_id = inWhitchRoom(userid,rooms)
    if room_id is None:
        emit('processWrong',{'status':NOT_IN_ROOM},to=request.sid)
        return
    room:RoomManager = fetchRoomByRoomID(room_id,rooms)
    game:GameTable = room.game_table
    if game is None:
        emit('processWrong',{'status':NOT_JOIN_GAME},to=request.sid)
        return
    try:
        status = game.movePiece(userid, x1, y1, z1, x2, y2, z2)
        if status != SUCCESS and status != GAME_END:
            emit('processSuccess',{'status':status},to=request.sid)
            return
        else:
            # 建议前端根据userid来判断到底是自己走成功了，还是其他人走的，自己这边要更新状态
            emit('movePieceSuccess',{'userid':userid,'status':status, 'username':sessions[userid],
                                     'x1':x1, 'y1':y1, 'z1':z1, 
                                     'x2':x2, 'y2':y2, 'z2':z2},
                                     to=room_id)
            if status == GAME_END:
                roomOver(game=game, room=room, userid=game.winner_id)
            return
    except Exception as e:
        emit('processWrong',{'status':OTHER_ERROR},to=request.sid)
        return 

def roomOver(game:GameTable, room:RoomManager, userid:int):
    global rooms,sessions
    # 获取当前的房间类型0是创建房间，1是匹配，2是排位   
    room_type = 0
    if room.room_type == RoomType.matched:
        room_type = 1
    elif room.room_type == RoomType.ranked: 
        room_type = 2
    # 游戏结束，判断胜利者或平局
    if game.game_state == EnumGameState.win:
        # 记录结束时间
        game.record.end_time = datetime.datetime.now()
        # 通知所有玩家游戏结束并告知胜利者
        logger.info(f"Game {game.game_id} end, winner is {sessions[userid] if userid in sessions else 'None'}")
        print(game.record.end_time)
        print(game.record.start_time)
        match_duration = (game.record.end_time - game.record.start_time)
        print(f"对局时长为：{match_duration}")
        emit('gameEnd', {'status': GAME_END, 'room_type':room_type,"step_count":game.step_count,"match_duration": match_duration.total_seconds(),'winner': userid, 'winner_name': sessions[userid]}, to=room.room_id)
        # 结束记录
        game.record.recordEnd(userid)

    elif game.game_state == EnumGameState.draw:
        # 记录结束时间
        game.record.end_time = datetime.datetime.now()
        # 通知所有玩家游戏结束为平局
        logger.info(f"Game {game.game_id} end, winner is {sessions[userid] if userid in sessions else 'None'}")
        match_duration = (game.record.end_time - game.record.start_time)
        emit('gameEnd', {'status': GAME_END, 'room_type':room_type,"step_count":game.step_count,"match_duration": match_duration,'winner': -1, 'winner_name': None}, to=room.room_id)
        # 结束记录
        game.record.recordEnd(None)

    room.removeGameTable()
    if room.room_type == RoomType.matched:
        try:
            logger.info(f"Remove room {room.room_id} after game end")
            rooms.remove(room)
            close_room(room=room.room_id,namespace='/')
        except Exception as e:
            logger.error("May remove in other way. Remove room error due to {0}".format(str(e)), exc_info=True)

@socketio.event
def watchGame(data):
    """
    请求观战，前提是游戏已经开始
    Args:
        userid: 用户id          int
        room_id: 房间id        str
    """
    global rooms
    params = {'userid':int,  'room_id':str}
    try:
        userid,room_id = getParams(params,data)
    except:
        emit('processWrong',{'status':PARAM_ERROR},to=request.sid)
        return
    # 注意要将sid2uid映射到userid
    sid2uid[request.sid] = userid
    try:
        room = fetchRoomByRoomID(room_id,rooms)
        if room is None or room.game_table is None:
            emit('processWrong',{'status':ROOM_NOT_EXIST},to=request.sid)
            return
        user = UserDict(userid=userid,username=sessions[userid])
        if room.game_table.addViewer(user):
            room.addUser(user) 
            join_room(room_id)
            logger.info(f"User {userid} watch game {room.game_table.game_id} and join room {room_id}")
            # 需要前端根据自己的身份来决定是成功加入观战，还是某某进入观战
            emit('watchGameSuccess',{'room_id':room_id,'game_info':room.game_table.getGameInfo()},to=room_id,namespace='/')
        else:
            emit('processWrong',{'status':NOT_JOIN_GAME},to=request.sid)
    except Exception as e:
        logger.error("Watch game error due to {0}".format(str(e)), exc_info=True)
        emit('processWrong',{'status':OTHER_ERROR},to=request.sid)
        return 

@socketio.event
def requestSurrender(data):
    """
    接收玩家投降请求的数据。
    Args:
        userid: 用户id          int 
    """
    global rooms,sessions
    params = {'userid': int}
    try:
        userid = getParams(params,data)
    except:
        emit('processWrong',{'status':PARAM_ERROR},to=request.sid)
        return

    # 先判断用户是否在房间中
    room_id = inWhitchRoom(userid, rooms)
    if room_id is None:
        emit('processWrong',{'status':NOT_IN_ROOM},to=request.sid)
        return
    room = fetchRoomByRoomID(room_id, rooms)
    game: GameTable = room.game_table
    if game is None:
        emit('processWrong',{'status':NOT_JOIN_GAME},to=request.sid)
        return

    try:
        # 玩家投降
        status = game.surrender(userid)

        # 通知所有玩家有玩家投降
        emit('surrenderSuccess',{'userid':userid,'username':sessions[userid],'game_info':game.getGameInfo()},to=room_id)
        # 判断游戏是否结束
        if status == GAME_END:
            roomOver(game=game, room=room, userid=game.winner_id)
        
    except Exception as e:
        logger.error("Request surrender error due to {0}".format(str(e)), exc_info=True)
        emit('processWrong',{'status':OTHER_ERROR},to=request.sid)


@socketio.event
def requestDraw(data):
    """
    接收玩家发起求和请求的数据。
    Args:
        userid: 用户id          int 
    """
    global rooms
    params = {'userid':int}
    try:
        userid = getParams(params,data)
    except:
        emit('processWrong',{'status':PARAM_ERROR},to=request.sid)
        return
    # 先判断用户是否在房间中
    room_id = inWhitchRoom(userid,rooms)
    if room_id is None:
        emit('processWrong',{'status':NOT_IN_ROOM},to=request.sid)
        return
    game:GameTable = fetchRoomByRoomID(room_id,rooms).game_table
    if game is None:
        emit('processWrong',{'status':NOT_JOIN_GAME},to=request.sid)
        return
    try:
        game.requestDraw(userid)
        # 广播求和请求给其他存活的玩家
        for user in game.getAlivePlayers():
            if user != userid:
                emit('drawRequest', {'requester': userid}, to=user)
        return
    except Exception as e:
        emit('processWrong',{'status':OTHER_ERROR},to=request.sid)
        return 
    
@socketio.event
def respondDraw(data):
    """
    接收玩家回应求和请求的数据。
    Args:
        userid: 用户id          int 
        agree: 玩家是否同意求和  bool
    """
    global rooms
    params = {'userid':int,  'agree':bool}
    try:
        userid, agree = getParams(params,data)
    except:
        emit('processWrong',{'status':PARAM_ERROR},to=request.sid)
        return
    # 先判断用户是否在房间中
    room_id = inWhitchRoom(userid,rooms)
    if room_id is None:
        emit('processWrong',{'status':NOT_IN_ROOM},to=request.sid)
        return
    game:GameTable = fetchRoomByRoomID(room_id,rooms).game_table
    if game is None:
        emit('processWrong',{'status':NOT_JOIN_GAME},to=request.sid)
        return
    try:
        # 通知所有玩家游戏结束
        game.respondDraw(userid, agree)
        # 所有存活的玩家均已回应
        if len(game.draw_respondents) == len(game.getAlivePlayers):
            for res_agree in game.draw_agree:
                if res_agree == False:
                    for user in game.getAlivePlayers:
                        emit('gameOngoing', {'status': SUCCESS}, to=user)
                    game.setDraw()
                    return
            for user in game.users:
                emit('gameEnd', {'status': GAME_END, 'winner': -1}, to=room_id)
            game.setDraw()
        else:
            emit('wait_for_others', {'status': SUCCESS}, to=user)
        return
    except Exception as e:
        emit('processWrong',{'status':OTHER_ERROR},to=request.sid)
        return 

def cycleMatch(app):
    """
    匹配模式下，定时检查的守护进程，检查是否有玩家加入匹配队列，若有则创建房间
    """
    global rooms, match_queue, sessions
    with app.app_context():
        while True:
            if match_queue.qsize() >= 3:
                user0,user1,user2 = match_queue.get(),match_queue.get(),match_queue.get()
                try:
                    # 开始游戏
                    room = RoomManager([UserDict(userid=user0,username=sessions[user0]),UserDict(userid=user1,username=sessions[user1]),UserDict(userid=user2,username=sessions[user2])],RoomType.matched)
                    rooms.append(room)
                    
                    room.game_table = GameTable(room.users)

                    for user in room.users:
                        join_room(room=room.room_id,sid=uid2sid(user['userid']),namespace='/')

                    logger.info(f"Create room : {room.room_id} and game: {room.game_table.game_id}")
                    # 通知房间所有人匹配到了
                    emit('startMatchSuccess',{'game_id':room.game_table.game_id,
                                            'room_info':room.getRoomInfo()},
                                            to=room.room_id,namespace='/')
                except Exception as e:
                    logger.error("Create match_game error due to {0}".format(str(e)), exc_info=True)
                    for user in [user0,user1,user2]:
                        if user and user in sessions:
                            match_queue.put(user)
                    if room and room in rooms:
                        rooms.remove(room)
                    
            time.sleep(1)

def cycleRank(app):
    """
    排位模式下，定时检查的守护进程，检查是否有玩家加入排位队列，若有则创建房间
    """
    global rooms, rank_queue, sessions
    with app.app_context():
        while True:
            def is_eligible(user1, user2):
                rank_diff = abs(user1[1] - user2[1])
                points_diff = abs(user1[2] - user2[2])
                return rank_diff <= 1 and points_diff <= 100  # 假设允许的最大段位差和积分差

            if rank_queue.qsize() >= 3:
                user_list = []
                for _ in range(rank_queue.qsize()):
                    user_list.append(rank_queue.get())

                eligible_users = []
                # 将段位符合的[user1，user2]组加入到eligible_users中
                for i, user1 in enumerate(user_list):
                    for j, user2 in enumerate(user_list[i+1:], start=i+1):
                        if user1 != user2 and is_eligible(user1, user2):
                            eligible_users.append([user1, user2])

                # 再遍历user_list，将各个user与eligible_users中的各组中的两个user分别进行比对
                # 第一组段位符合的 3 个玩家进行匹配
                matched_users = None
                for [user1, user2] in eligible_users:
                    for user in user_list:
                        if user != user1 and user != user2 and is_eligible(user, user1) and is_eligible(user, user2):
                            matched_users = (user1, user2, user)
                            break
                    if matched_users is not None:
                        break
                if matched_users is not None:
                    user0, user1, user2 = matched_users
                    # 将除此 3 人外所有用户放回队列
                    for user in user_list:
                        if user and user != user0 and user != user1 and user != user2 and user in sessions:
                            rank_queue.put(user)
                    try:
                        # 开始游戏
                        room = RoomManager([UserDict(userid=user0[0], username=sessions[user0[0]]),
                                            UserDict(userid=user1[0], username=sessions[user1[0]]),
                                            UserDict(userid=user2[0], username=sessions[user2[0]])], room_type='ranked')
                        rooms.append(room)
                        room.game_table = GameTable([user['userid'] for user in room.users])
                        for user in room.users:
                            join_room(room=room.room_id, sid=uid2sid(user['userid']))
                        logger.info(f"Create room : {room.room_id} and game: {room.game_table.game_id}")
                        # 通知房间所有人匹配到了
                        emit('startRankSuccess', {'room_id': room.room_id, 'game_id': room.game_table.game_id,
                                                            'users': [room.users[0].userid, room.users[1].userid, room.users[2].userid],
                                                            'usernames': [room.users[0].username, room.users[1].username, room.users[2].username],
                                                            'ranks': [user0[1], user1[1], user2[1]],
                                                            'points': [user0[2], user1[2], user2[2]]},
                                to=room.room_id, namespace='/')
                    except Exception as e:
                        logger.error("Create rank_game error due to {0}".format(str(e)), exc_info=True)
                        for user in [user0,user1,user2]:
                            if user and user in sessions:
                                rank_queue.put(user)
                        if room and room in rooms:
                            rooms.remove(room)
                else:
                    # 重新将所有用户放回队列
                    for user in user_list:
                        if user and user in sessions:
                            rank_queue.put(user)

            time.sleep(1)

@socketio.event
def startMatch(data):
    """
    接收玩家开始匹配请求
    Args:
        userid: 用户id      int 
    """
    global match_queue
    params = {'userid':int}
    try:
        userid = getParams(params,data)
    except:
        emit('processWrong',{'status':PARAM_ERROR},to=request.sid)
        return
    sid2uid[request.sid] = userid # 维护sid2uid映射
    match_queue.put(userid)
    logger.info(f"User {userid} join match queue: sid {request.sid}")

@socketio.event
def startRankedMatch(data):
    """
    接收玩家开始排位匹配请求
    Args:
        userid: 用户id      int 
    """
    global rooms, rank_queue
    params = {'userid': int}
    try:
        userid = getParams(params, data)
    except:
        emit('processWrong', {'status': PARAM_ERROR}, to=request.sid)
        return

    # 获取玩家的段位和积分
    result = viewUserRank(userid)
    if not result:
        emit('processWrong', {'status': OTHER_ERROR}, to=request.sid)
        return
    
    user_rank, user_points = result
    sid2uid[request.sid] = userid # 维护sid2uid映射
    rank_queue.put((userid, user_rank, user_points))
    logger.info(f"User {userid} join rank queue: sid {request.sid}")

@socketio.event
def viewGameRecords(data):
    """
    接收玩家查看对局记录请求
    Args:
        userid: 用户id      int 
    """
    params = {'userid':int}
    try:
        userid = getParams(params,data)
    except:
        emit('processWrong',{'status':PARAM_ERROR},to=request.sid)
        return
    try:
        # 查询游戏记录
        records = viewUserGameRecords(userid)
        logger.info(records)
        emit('gameRecord', {'record': records}, to=request.sid)
    except Exception as e:
        emit('processWrong',{'status':OTHER_ERROR},to=request.sid)
        logger.error(e)
        return 

@socketio.event
def viewMoveRecords(data):
    """
    接收玩家查看对局移动记录请求
    Args:
        record_id: 对局id      int 
    """
    params = {'record_id':int}
    try:
        record_id = getParams(params,data)
    except:
        emit('processWrong',{'status':PARAM_ERROR},to=request.sid)
        return
    try:
        # 查询游戏记录
        records = viewGameMoveRecords(record_id)
        logger.info(records)
        emit('gameMoveRecord', {'record': records}, to=request.sid)
    except Exception as e:
        emit('processWrong',{'status':OTHER_ERROR},to=request.sid)
        logger.error(e)
        return


if __name__ == "__main__":
    threading.Thread(target=cycleMatch,args=[app] ,daemon=True, name='cycleMatch').start()
    socketio.run(app,debug=True,host='0.0.0.0',port=8888,allow_unsafe_werkzeug=True)
    print("Good bye!")