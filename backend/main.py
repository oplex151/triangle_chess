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
from backend.log_tool import setupLogger 
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
    try:
        username = request.form.get('username')
        password = request.form.get('password')
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
    try:
        username = request.form.get('username')
        password = request.form.get('password')
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
    try:
        userid = request.form.get('userid')
        print(userid)
    except:
        return "{message: 'parameter error'}",PARAM_ERROR
    return logout(userid)


@app.route('/api/game/create', methods=['POST'])
def createGameApi():
    '''
    Args:
        user1id: 用户1id 房主

        room_id: 房间id
    Returns:
        成功返回200
    '''
    global rooms
    try:
        user1id = request.form.get('user1id') # TODO::检查房主是否存在
        room_id = request.form.get('room_id')
    except:
        return "{message: 'parameter error'}",PARAM_ERROR
    try:
        print(room_id)
        room = fetchRoomByRoomID(room_id,rooms)
        if room is None:
            return "{message: '房间不存在！'}",ROOM_NOT_EXIST
        if len(room.users) != 3:
            return "{message: '房间人数不足！'}",ROOM_NOT_ENOUGH
        game = GameTable(room.users) # TODO::这里应该是创建游戏
        room.addGameTable(game)
        emit('createGameSuccess',{'game_id':game.game_id},to=room_id,namespace='/')
        logger.info("Create game: {0}".format(game.game_id))
        return (),SUCCESS
    except Exception as e:
        logger.error("Create game error due to {0}".format(str(e)), exc_info=True)
        return "{message: 'create game error'}",GAME_CREATE_FAILED


@socketio.event
def movePiece(data):
    '''
    Args:
        userid: 用户id
        chess_type: 棋子类型
        x1: 起始横坐标
        y1: 起始纵坐标
        z1: 起始棋盘
        x2: 目标横坐标
        y2: 目标纵坐标
        z2: 目标棋盘
    Returns:
        移动成功200
    '''
    try:
        userid = data.get('userid')
        chess_type = data.get('chess_type')
        x1 = data.get('x1')
        y1 = data.get('y1')
        z1 = data.get('z1') 
        x2 = data.get('x2')
        y2 = data.get('y2')
        z2 = data.get('z2')
    except:
        return "{message: 'parameter error'}",PARAM_ERROR
    game:GameTable = fetchGameByUserID(userid)
    if game is None:
        return "{}",NOT_JOIN_GAME
    try:
        status = game.movePiece(userid, chess_type, x1, y1, z1, x2, y2, z2)
        return "{}",status
    except Exception as e:
        return "{message: {0}}".format(str(e)),OTHER_ERROR

@socketio.on('connect')
def establishConnection():
    '''
    建立socket连接
    Args:
        userid: 用户id
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
        userid: 用户id 作为房主
    '''
    global rooms,sid2uid
    userid = data['userid']
    room_id = inWhitchRoom(userid,rooms)
    if room_id is not None:
        logger.error("User {0} is already in room {1}".format(userid,room_id))
        emit('processWrong',{'status':ALREADY_IN_ROOM},to=request.sid)
        return
    new_room = RoomManager(int(userid))
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
        room_id: 房间id
        userid: 用户id
    '''
    global rooms
    try:
        room_id = data['room_id']
        userid = data['userid']
    except:
        logger.error("Join room error", exc_info=True)
        emit('processWrong',{'status':PARAM_ERROR},to=request.sid)
        return
    
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
    # 已经在这个房间中, 不可以重复加入
    elif tmp_id is not None: 
        logger.info(f"User {userid} already in room {room_id}"+
                    f"this room's users: {fetchRoomByRoomID(room_id,rooms).users}")
        emit('processWrong',{'status':ALREADY_IN_ROOM},to=request.sid)
        return
    else:
        if room.game_table is not None and room.game_table.searchGameTable(userid):
            # 用户在游戏中
            logger.info(f"User {userid} reconnect to game {room.game_table.game_id}")
    
    # if room.isFull():
    #     logger.error("Room {0} is full".format(room_id))
    #     emit('processWrong',status=ROOM_FULL,to=request.sid)
    room.addUser(int(userid))
    join_room(room_id)
    logger.info(f"User {userid} join room {room_id}, sid={request.sid}"
                +f"this room's users: {room.users}")
    emit('joinRoomSuccess',to=room_id)
    # 更新sid2uid
    if request.sid not in sid2uid: 
        sid2uid[request.sid] = userid

@socketio.event
def leaveRoom(data):
    '''
    Description: 离开房间
    Args:
        room_id: 房间id
        userid: 用户id
    '''
    global rooms,sid2uid
    try:
        room_id = data['room_id']
        userid = data['userid']
    except:
        logger.error("Leave room error", exc_info=True)
        emit('processWrong',{'status':PARAM_ERROR},to=request.sid)
        return
    room:RoomManager = fetchRoomByRoomID(room_id,rooms)
    if room is None:
        logger.error("No such room {0}".format(room_id))
        emit('processWrong',{'status':ROOM_NOT_EXIST},to=request.sid)
        return
    if room.removeUser(int(userid)):
        emit('leaveRoomSuccess',{'userid':sid2uid[request.sid]},to=room_id)
        logger.info(f"User {userid} leave room {room_id}, sid={request.sid}"
                    +f"this room's users: {room.users}")
        leave_room(room_id)
        # 更新sid2uid
        if request.sid in sid2uid:
            sid2uid.pop(request.sid)
    else:
        logger.error("User {0} not in room {1}".format(userid,room_id))
        emit('processWrong',{'status':NOT_IN_ROOM},to=request.sid)

# TODO::重新连接

@socketio.event
def sendMessage(data):
    '''test'''
    room_id = data['room_id']
    userid = data['userid']
    message = data['message']
    emit('receiveMessage',{'message':message},userid=userid,to=room_id,
         skip_sid=request.sid)

if __name__ == "__main__":
    socketio.run(app,debug=True,host='0.0.0.0',port=8888)
    print("Good bye!")