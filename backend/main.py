import os
import sys
from pathlib import Path
import threading

project_root = Path(__file__).parent.parent.absolute()
os.environ['PROJECT_ROOT'] = str(project_root)
sys.path.append(str(Path(__file__).resolve().parent.parent))
print("Project root set to:", os.environ['PROJECT_ROOT']) # 设置项目根目录

import flask
from flask_socketio import SocketIO,join_room,leave_room,emit
from flask_cors import CORS
from flask import request
from backend.global_var import *
from backend.tools import setupLogger, get_params
from backend.user_manage import *
from backend.game.exception import *
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
        username,password = get_params(params,request.form)
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
        username,password = get_params(params,request.form)
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
        userid = get_params(params,request.form)
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
    if request.sid in sid2uid:
        # 断开连接时,判断用户是否在房间中,如果在房间中,则退出房间
        userid = sid2uid[request.sid] 
        room_id = inWhitchRoom(userid,rooms)
        if room_id is not None:
            logger.info(f"User {userid} leave room {room_id}"+
                        f"this room's users: {fetchRoomByRoomID(room_id,rooms).users}")
            room = fetchRoomByRoomID(room_id,rooms)
            room.removeUser(userid)
            leave_room(room.room_id)
        sid2uid.pop(request.sid)
    logger.info("User {0} disconnect".format(request.sid))

@socketio.event
def createRoom(data):
    '''
    Description: 创建房间
    Args:
        userid: 用户id 作为房主 int
    '''
    global rooms,sid2uid
    params = {'userid':int}
    try:
        userid = get_params(params,data)
    except:
        emit('processWrong',{'status':PARAM_ERROR},to=request.sid)
        return
    
    room_id = inWhitchRoom(userid,rooms)
    if room_id is not None:
        logger.error("User {0} is already in room {1}".format(userid,room_id))
        emit('processWrong',{'status':ALREADY_IN_ROOM},to=request.sid)
        return
    new_room = RoomManager(userid)
    rooms.append(new_room)
    room_id = rooms[-1].room_id
    join_room(room_id)
    logger.info(f"Create room {room_id} by user {userid}, sid={request.sid}\n"
                +f"this room's users: {new_room.users}")
    emit('createRoomSuccess',{'room_id':room_id},to=request.sid)
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
    global rooms,sessions
    parms = {'room_id':str, 'userid':int}
    try:
        room_id,userid = get_params(parms,data)
    except:
        logger.error("Join room error", exc_info=True)
        emit('processWrong',{'status':PARAM_ERROR},to=request.sid)
        return
    logger.info(f"User {userid} join room {room_id}")
    room = fetchRoomByRoomID(room_id,rooms)
    if room is None:
        logger.error("No such room {0}".format(room_id))
        emit('processWrong',{'status':ROOM_NOT_EXIST},to=request.sid)
        return
    # 查询该用户是否在某个房间中
    tmp_id = inWhitchRoom(userid,rooms)
    # 已经在某个房间中, 先退出
    if tmp_id is not None and tmp_id != room_id: 
        logger.info(f"User {userid} leave room {tmp_id}"+
                    f"this room's users: {fetchRoomByRoomID(tmp_id,rooms).users}")
        room = fetchRoomByRoomID(tmp_id,rooms)
        room.removeUser(userid)
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
        emit('initGame',{'game_info':room.game_table.getGameInfo()},to=room_id,namespace='/')
    
    room.addUser(userid)
    join_room(room_id)
    logger.info(f"User {userid} join room {room_id}, sid={request.sid}"
                +f"this room's users: {room.users}")
    emit('joinRoomSuccess',{'room_id':room_id,'userid':userid,'username':sessions[userid]},to=room_id)
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
    global rooms,sid2uid
    parms = {'room_id':str, 'userid':int}
    try:
        room_id,userid = get_params(parms,data)
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
        emit('leaveRoomSuccess',{'userid':sid2uid[request.sid]},to=room_id)
        leave_room(room_id)
        # 更新sid2uid
        if request.sid in sid2uid:
            sid2uid.pop(request.sid)
        # 房间为空, 移除房间
        if len(room.users) == 0:
            rooms.remove(room)
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
        userid,room_id = get_params(params,request.form) # TODO::检查房主是否存在
    except:
        return "{message: 'parameter error'}",PARAM_ERROR
    try:
        print(room_id)
        room = fetchRoomByRoomID(room_id,rooms)
        if room is None:
            return "{message: '房间不存在！'}",ROOM_NOT_EXIST
        if len(room.users) < 3:
            return "{message: '房间人数不足！'}",ROOM_NOT_ENOUGH
        for user in room.users[:3]:
            if user < 0:
                return "{message: '房间人数不足！'}",ROOM_NOT_ENOUGH
        
        game:GameTable = GameTable(room.users[:3]) # TODO::这里应该是创建游戏
        room.addGameTable(game)
        logger.info(f"join user {room.users[:3]} in room {game.game_id}")
        emit('createGameSuccess',{'game_id':game.game_id,'users':[room.users[0],room.users[1],room.users[2]],'usernames':[sessions[room.users[0]],sessions[room.users[1]],sessions[room.users[2]]]},to=room_id,namespace='/')
        emit('initGame',{'game_info':game.getGameInfo()},to=room_id,namespace='/')
        logger.info("Create game: {0}".format(game.game_id))
        return "{}",SUCCESS
    except Exception as e:
        logger.error("Create game error due to {0}".format(str(e)), exc_info=True)
        return "{message: 'create game error'}",GAME_CREATE_FAILED

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
    global rooms
    params = {'userid':int,  'x1':int, 'y1':int, 'z1':int, 'x2':int, 'y2':int, 'z2':int}
    try:
        userid,x1,y1,z1,x2,y2,z2 = get_params(params,data)
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
            emit('movePieceSuccess',{'userid':userid,'status':status, 
                                     'x1':x1, 'y1':y1, 'z1':z1, 
                                     'x2':x2, 'y2':y2, 'z2':z2},
                                     to=room_id)
            if status == GAME_END:
                roomOver(game=game, room=room, userid=userid)
            return
    except Exception as e:
        emit('processWrong',{'status':OTHER_ERROR},to=request.sid)
        return 

def roomOver(game:GameTable, room:RoomManager, userid:int):
    # 游戏结束，判断胜利者或平局
    if game.game_state == EnumGameState.win:
        # 通知所有玩家游戏结束并告知胜利者
        logger.info(f"Game {game.game_id} end, winner is {userid}")
        emit('gameEnd', {'status': GAME_END, 'winner': userid, 'winner_name': sessions[userid]}, to=room.room_id)
    elif game.game_state == EnumGameState.draw:
        # 通知所有玩家游戏结束为平局
        logger.info(f"Game {game.game_id} end, winner is {userid}")
        emit('gameEnd', {'status': GAME_END, 'winner': -1, 'winner_name': None}, to=room.room_id)
    room.removeGameTable()
    if room.room_type == RoomType.matched:
        # 匹配模式下，游戏结束后，关闭房间
        # 请前端自行处理匹配模式下的后续操作
        rooms.remove(room)

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
        userid = get_params(params,data)
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
        game.request_draw(userid)
        # 广播求和请求给其他存活的玩家
        for user in game.get_alive_players():
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
        userid, agree = get_params(params,data)
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
        game.respond_draw(userid, agree)
        # 所有存活的玩家均已回应
        if len(game.draw_respondents) == len(game.get_alive_players):
            for res_agree in game.draw_agree:
                if res_agree == False:
                    for user in game.get_alive_players:
                        emit('gameOngoing', {'status': SUCCESS}, to=user)
                    game.set_draw()
                    return
            for user in game.users:
                emit('gameEnd', {'status': GAME_END, 'winner': -1}, to=room_id)
            game.set_draw()
        else:
            emit('wait_for_others', {'status': SUCCESS}, to=user)
        return
    except Exception as e:
        emit('processWrong',{'status':OTHER_ERROR},to=request.sid)
        return 

@socketio.event
def startMatch(data):
    """
    接收玩家开始匹配请求
    Args:
        userid: 用户id      int 
    """
    global rooms, match_queue
    params = {'userid':int}
    try:
        userid = get_params(params,data)
    except:
        emit('processWrong',{'status':PARAM_ERROR},to=request.sid)
        return
    match_queue.put(userid)
    if (match_queue.qsize() >= 3):
        user0,user1,user2 = match_queue.get(),match_queue.get(),match_queue.get()
        # 开始游戏
        room = RoomManager([user0,user1,user2],RoomType.matched)
        rooms.append(room)
        room.game_table = GameTable(room.users)
        for user in room.users:
            join_room(room=room.room_id,sid=uid2sid(user))
        logger.info(f"Create room : {room.room_id} and game: {room.game_table.game_id}")
        emit('startMatchSuccess',{'room_id':room.room_id,'game_id':room.game_table.game_id,
                                  'users':[room.users[0],room.users[1],room.users[2]],
                                  'usernames':[sessions[room.users[0]],sessions[room.users[1]],sessions[room.users[2]]]},
                                  to=room.room_id,namespace='/')
        emit('initGame',{'game_info':room.game_table.getGameInfo()},to=room.room_id,namespace='/')

# TODO::重新连接

if __name__ == "__main__":
    socketio.run(app,debug=True,host='0.0.0.0',port=8888,allow_unsafe_werkzeug=True)
    print("Good bye!")