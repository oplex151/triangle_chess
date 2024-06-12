import os
import sys
from pathlib import Path
import threading
import time
import heapq
project_root = Path(__file__).parent.parent.absolute()
os.environ['PROJECT_ROOT'] = str(project_root)
sys.path.append(str(Path(__file__).resolve().parent.parent))
print("Project root set to:", os.environ['PROJECT_ROOT']) # 设置项目根目录

import jwt
import flask
from flask_socketio import SocketIO,join_room,leave_room,emit,close_room
from flask_cors import CORS
from flask import request
from backend.global_var import *
from backend.tools import setupLogger, getParams
from backend.user_manage import *
from backend.user_manage.appeal import *
from backend.tools.exception import *
from backend.game.record import *
from message import *
from backend.game import *
from backend.tools.exception import *

app = flask.Flask(__name__)
CORS(app,cors_allowed_origins="*")
app.config['SECRET_KEY'] = 'sanguoxiangqi'
socketio = SocketIO(app, cors_allowed_origins="*")

# 日志工具
logger = setupLogger()

def gate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        global session_times,sessions
        try:
            if len(args) == 0:  #http
                userid = request.form.get('userid')
            else:  #websocket
                userid = args[0].get('userid')

            if not isinstance(userid,int) and userid is not None:
                userid = int(userid)

            if userid is None or userid not in sessions.keys():
                logger.debug('session expired! '+'func name:'+func.__name__) 
                raise SessionException
            
            session_times[userid] = time.time() # 更新session时间
            return func(*args, **kwargs)
        
        except SessionException:
            if len(args) == 0:  #http
                return "{message: 'session expired!'}",SESSION_EXPIRED
            else:  #websocket
                emit('processWrong',{'status':SESSION_EXPIRED},to=request.sid,namespace='/')
                return 
        except Exception as e: 
            logger.error(e,exc_info=True)
            if len(args) == 0:  #http
                return "{message: 'session expired!'}",SESSION_EXPIRED
            else:  #websocket
                emit('processWrong',{'status':SESSION_EXPIRED},to=request.sid,namespace='/')
                return
    return wrapper

def protectedAdmin(token):
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'],algorithms=['HS256'])
        # 验证成功，可以提取信息
        print('Authenticated',payload)
        return True
    except jwt.ExpiredSignatureError:
        print('Token过期')
        return False
    except jwt.InvalidTokenError:
        print('Token无效')
        return False

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
        email: 邮箱
        phone_num:手机号
        gender:性别
    Returns:
        注册成功200
    '''
    params = {'username':str, 'password':str, 'email':str, 'phone_num':str, 'gender':str}
    try:
        username,password,email,phone_num,gender = getParams(params,request.form,['email','phone_num','gender'])
    except:
        return "{message: 'parameter error'}",PARAM_ERROR
    return register(username, password, email, phone_num, gender)

@app.route('/api/uploadImage', methods=['POST'])
@gate
def uploadImageApi():
    '''
    Description: 上传图片
    Args:
        userid: 用户id
        image: 图片文件
    Returns:
        上传成功200
    '''
    params = {'userid':int, 'image':str}
    try:
        userid,image = getParams(params,request.form)
    except:
        return "{message: 'parameter error'}",PARAM_ERROR
    return uploadImage(userid, image)


@app.route('/api/changeUserInfo', methods=['POST'])
@gate
def changeUserInfoApi():
    '''
    Description: 修改用户信息
    Args:
        userid: 用户id
        username: 用户名
        email: 邮箱
        phone_num:手机号
        gender:性别
    Returns:
        修改成功200
    '''
    params = {'userid':int, 'username':str, 'email':str, 'phone_num':str, 'gender':str}
    try:
        userid,username,email,phone_num,gender = getParams(params,request.form,['username','email','phone_num','gender'])
    except:
        return "{message: 'parameter error'}",PARAM_ERROR
    return changeUserInfo(userid, username, email, phone_num, gender)

@app.route('/api/changePassword', methods=['POST'])
@gate
def changePasswordApi():
    '''
    Description: 修改密码
    Args:
        userid: 用户id
        old_password: 旧密码
        new_password: 新密码
    Returns:
        修改成功200
    '''
    params = {'userid':int, 'old_password':str, 'new_password':str}
    try:
        userid,old_password,new_password = getParams(params,request.form)
    except:
        return "{message: 'parameter error'}",PARAM_ERROR
    return changePassword(userid, old_password, new_password)

@app.route('/api/adminLogin',methods=['POST'])
def adminLoginApi():
    '''
    Description: 管理员登录
    Args:
        password: 密码
    Returns:
        登录成功200
    '''
    params = {'password':str}
    try:
        password = getParams(params,request.form)
    except:
        return "{message: 'parameter error'}",PARAM_ERROR
    return adminLogin(password,app.config['SECRET_KEY'])

@app.route('/api/checkAdmin',methods=['POST'])
def checkAdminApi():
    '''
    Description: 检查管理员权限
    Args:
        token: token
    Returns:
        权限验证成功200
    '''
    params = {'token':str}
    try:
        token = getParams(params,request.form)
    except:
        return "{message: 'parameter error'}",PARAM_ERROR
    if protectedAdmin(token):
        return "{message: 'admin'}",SUCCESS
    else:
        return "{message: 'not admin'}",NOT_ADMIN

@app.route('/api/getUserData', methods=['POST'])
def getUserDataApi():
    '''
    Description: 获取用户数据
    Args:
        token: token
    Returns:
        用户数据 详见数据库user表
    '''
    params = {'token':str}
    try:
        token = getParams(params,request.form)
    except:
        return "{message: 'parameter error'}",PARAM_ERROR
    if protectedAdmin(token):
        return getUserData()
    else:
        return "{message: 'not admin'}",NOT_ADMIN
    
@app.route('/api/banUser', methods=['POST'])
def banUserApi():
    '''
    Description: 封禁用户
    Args:
        token: token
        userid: 用户id
    Returns:
        封禁成功200
    '''
    params = {'token':str, 'userid':int}
    try:
        token,userid = getParams(params,request.form)
    except:
        return "{message: 'parameter error'}",PARAM_ERROR
    if protectedAdmin(token):
        return changeUserBanned(userid, 1)
    else:
        return "{message: 'not admin'}",NOT_ADMIN

@app.route('/api/releaseUser', methods=['POST'])
def releaseUserApi():
    '''
    Description: 解封用户
    Args:
        token: token
        userid: 用户id
    Returns:
        解封成功200
    '''
    params = {'token':str, 'userid':int}
    try:
        token,userid = getParams(params,request.form)
    except:
        return "{message: 'parameter error'}",PARAM_ERROR
    if protectedAdmin(token):
        return changeUserBanned(userid, 0)
    else:
        return "{message: 'not admin'}",NOT_ADMIN

@app.route('/api/logout', methods=['POST'])
@gate
def logoutApi():
    '''
    Description: 登出
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

@app.route('/api/getUserInfo', methods=['POST'])
def getUserInfoApi():
    '''
    Description: 获取用户信息
    Args:
        userid: 用户id
    Returns:
        用户信息 详见数据库user表
    '''
    params = {'userid':int}
    try:
        userid = getParams(params,request.form)
    except:
        return "{message: 'parameter error'}",PARAM_ERROR
    return getUserInfo(userid)

@app.route('/api/getRankInfo', methods=['POST'])
def getRankInfoApi():
    '''
    Description: 获取排行榜信息
    Args:
        userid: 用户id
    Returns:
        排行榜信息 详见数据库rank表
    '''
    params = {'userid':int}
    try:
        userid = getParams(params,request.form)
    except:
        return "{message: 'parameter error'}",PARAM_ERROR
    return getUserInfo(userid,['username','rank','score'])
    

@app.route('/api/addFriend', methods=['POST'])
@gate
def addFriendApi():
    '''
    Args:
        userid: 用户id
        friend_id: 好友id
    Returns:
        添加好友成功200
    '''
    params = {'userid':int, 'friend_id':int}
    try:
        userid,friend_id = getParams(params,request.form)
    except:
        return "{message: 'parameter error'}",PARAM_ERROR
    return addFriend(userid, friend_id)

@app.route('/api/getFriends', methods=['POST'])
def getFriendsApi():
    '''
    Args:
        userid: 用户id
    Returns:
        好友列表 详见数据库friend表
    '''
    params = {'userid':int, 'confirm':int}
    try:
        userid,confirm = getParams(params,request.form,['confirm'])
    except:
        return "{message: 'parameter error'}",PARAM_ERROR
    # 为confirm 赋默认值
    if confirm == None:
        confirm = 1
    return getFriendsInfo(userid,confirm)

@app.route('/api/deleteFriend',methods=['POST'])
@gate
def deleteFriendApi():
    '''
    Args:
        userid: 用户id
        friend_id: 好友id
    Returns:
        删除好友成功200
    '''
    params = {'userid':int, 'friend_id':int}
    try:
        userid,friend_id = getParams(params,request.form)
    except:
        return "{message: 'parameter error'}",PARAM_ERROR
    return deleteFriend(userid, friend_id)

@app.route('/api/confirmFriend',methods=['POST'])
@gate
def confirmFriendApi():
    '''
    Args:
        userid: 用户id
        friend_id: 好友id
        
    Returns:
        确认好友成功200
    '''
    params = {'userid':int, 'friend_id':int,'confirm':int}
    try:
        userid,friend_id,confirm= getParams(params,request.form,['confirm'])
    except:
        return "{message: 'parameter error'}",PARAM_ERROR
    return confirmFriend(userid, friend_id,confirm)

@app.route('/api/getRankScore',methods=['POST'])
@gate
def getRankScoreApi():
    '''
    Args:
        userid: 用户id
    Returns:
        用户的段位和积分
    '''
    params = {'userid':int}
    try:
        userid = getParams(params,request.form)
    except:
        return "{message: 'parameter error'}",PARAM_ERROR
    return getRankScore(userid)
    

@app.route('/api/addAppeals', methods=['POST'])
#@gate
def addAppealsApi():
    '''
    Args:
        userid: 用户id
        type: 申诉种类
        content: 申诉内容
        fromid: 申诉来源id
        username: 申诉来源用户名
        phone_number: 申诉来源手机号
    Returns:
        添加申诉成功200
    '''
    params = {'userid':int, 'type':str, 'content':str, 'fromid':int, 'username':str, 'phone_number':str}
    try:
        userid, appeal_type, content, fromid,username,phone_number = getParams(params,request.form,['type','content','fromid','username','phone_number'])
    except:
        return "{message: 'parameter error'}",PARAM_ERROR
    return addAppeals(userid, appeal_type, content, fromid, username, phone_number)

@app.route('/api/getAppeals', methods=['POST'])
def getAppealsApi():
    '''
    Args:
        token: token
    Returns:
        申诉列表 详见数据库appeal表
    '''
    params = {'token':str}
    try:
        token = getParams(params,request.form)
    except:
        return "{message: 'parameter error'}",PARAM_ERROR
    if protectedAdmin(token):
        return getAppealsInfo(None)
    else:
        return "{message: 'not admin'}",NOT_ADMIN

@app.route('/api/handleAppeal', methods=['POST'])
def handleAppealApi():
    '''
    Args:
        token: token
        appeal_id: 申诉id
        feedback: 处理结果
    Returns:
        处理申诉成功200
    '''
    params = {'token':str, 'appeal_id':int, 'feedback':str}
    try:
        token, appeal_id, feedback = getParams(params,request.form,['handle_result'])
    except:
        return "{message: 'parameter error'}",PARAM_ERROR
    if protectedAdmin(token):
        return handleAppeal(appeal_id, feedback)
    else:
        return "{message: 'not admin'}",NOT_ADMIN


@app.route('/api/getUserAppeal', methods=['POST'])
@gate
def getUserAppealApi():
    '''
    Args:
        userid: 用户id
    Returns:
        用户的申诉列表 详见数据库appeal表
    '''
    params = {'userid':int}
    try:
        userid = getParams(params,request.form)
    except:
        return "{message: 'parameter error'}",PARAM_ERROR
    return getAppealsInfo(userid)

@app.route('/api/getAvatars', methods=['POST'])
def getAvatarsApi():
    '''
    Args:
        userids: 用户ids
    Returns:
        用户头像列表 详见数据库avatar表
    '''
    params = {'userids':str}
    # logger.debug("getavatars:"+str(request.form))
    # logger.debug(request.form.getlist('userids[]'))
    try:
        userids = getParams(params,request.form)
    except:
        return "{message: 'parameter error'}",PARAM_ERROR
    # logger.debug("gettavatars:"+str(userids))
    userids = eval(userids)
    avatars,status = getSomeUserAvatar(userids)
    return jsonify(avatars),status

@app.route('/api/likeGameRecord', methods=['POST'])
def likeGameRecordApi():
    '''
    Args:
        recordid: 对局记录id
    Returns:
        点赞成功200
    '''
    params = {'recordid': int}
    try:
        recordid = getParams(params, request.form)
    except:
        return "{message: 'parameter error'}", PARAM_ERROR
    return likeGameRecord(recordid)

@app.route('/api/unlikeGameRecord', methods=['POST'])
def unlikeGameRecordApi():
    '''
    Args:
        recordid: 对局记录id
    Returns:
        取消点赞成功200
    '''
    params = {'recordid': int}
    try:
        recordid = getParams(params, request.form)
    except:
        return "{message: 'parameter error'}", PARAM_ERROR
    return unlikeGameRecord(recordid)

@app.route('/api/addComment', methods=['POST'])
@gate
def addCommentApi():
    '''
    Args:
        recordid: 对局记录id
        userid: 用户id
        content: 评论内容str
    Returns:
        添加评论成功200
    '''
    params = {'recordid': int, 'userid': int, 'content': str}
    try:
        recordid, userid, content = getParams(params, request.form)
    except:
        return "{message: 'parameter error'}", PARAM_ERROR
    return addComment(recordid, userid, content)

@app.route('/api/likeComment', methods=['POST'])
def likeCommentApi():
    '''
    Args:
        commentid: 评论id
    Returns:
        点赞成功200
    '''
    params = {'commentid': int}
    try:
        commentid = getParams(params, request.form)
    except:
        return "{message: 'parameter error'}", PARAM_ERROR
    return likeComment(commentid)

@app.route('/api/unlikeComment', methods=['POST'])
def unlikeCommentApi():
    '''
    Args:
        commentid: 评论id
    Returns:
        取消点赞成功200
    '''
    params = {'commentid': int}
    try:
        commentid = getParams(params, request.form)
    except:
        return "{message: 'parameter error'}", PARAM_ERROR
    return unlikeComment(commentid)

@app.route('/api/viewRecordComments', methods=['POST'])
def viewRecordCommentsApi():
    '''
    Args:
        recordid: 对局记录id
    Returns:
        评论列表
    '''
    params = {'recordid': int}
    try:
        recordid = getParams(params, request.form)
    except:
        return "{message: 'parameter error'}", PARAM_ERROR

    comments, status = viewRecordComments(recordid)
    return jsonify(comments), status

@app.route('/api/getAllRooms', methods=['POST'])
# @gate
def getAllRoomsApi():
    '''
    Args:
        userid: 用户id
    Returns:
        200

    '''
    global rooms
    rooms_copy = rooms.copy()
    rooms_to_return = [{'room_id':room.room_id,
                        'user_num':len(room.users) if len(room.users) <= 3 else 3,
                        'locked':room.locked,
                        'holder':{'username':room.holder['username'],'userid':room.holder['userid']},
                        'started': 1 if room.game_table is not None else 0,
                        'room_type': 1 if room.room_type == RoomType.matched else 2 if room.room_type == RoomType.ranked else 0
                        } for room in rooms_copy if room.room_type == RoomType.created]
    print(rooms_to_return)
    return jsonify({'rooms':rooms_to_return}),SUCCESS


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
    userid = None
    if request.sid in sid2uid:
        # 断开连接时,判断用户是否在房间中,如果在房间中,则退出房间
        userid = sid2uid[request.sid]
        sid2uid.pop(request.sid) 
        try:
            room_id = inWhitchRoom(userid,rooms)
            if room_id is not None:
                room:RoomManager = fetchRoomByRoomID(room_id,rooms)
                if room is not None:
                    if room.isHolder(userid) and room.game_table is None:
                        userids = [u['userid'] for u in room.users]
                        emit('leaveRoomSuccess',{'userid':-1},to=room.room_id,namespace='/',skip_sid=request.sid)

                        for u in userids:
                            sid = uid2sid(u)
                            if sid: 
                                leave_room(room_id,sid=sid) 
                                sid2uid.pop(sid)
                                
                        rooms.remove(room)
                        logger.info(f"Room {room_id} with no holder, so remove it")
                    else:
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
        
    logger.info("User {0} disconnect".format(request.sid) + ", userid=" + f"{userid}" if userid else "None")

@socketio.event
@gate
def createRoom(data):
    '''
    Description: 创建房间
    Args:
        userid: 用户id 作为房主 int
        locked: 是否锁定房间 int
        password: 房间密码 str
        time_interval: 房间时间间隔 int
    '''
    global rooms,sid2uid,sessions
    params = {'userid':int, 'locked':int, 'password':str , 'time_interval':int}
    try:
        userid, locked, password,time_interval = getParams(params, data, can_be_none=['locked','password','time_interval'])
    except:
        emit('processWrong',{'status':PARAM_ERROR},to=request.sid)
        return
    
    room_id = inWhitchRoom(userid,rooms)
    if room_id is not None:
        logger.error("User {0} is already in room {1}".format(userid,room_id))
        emit('processWrong',{'status':ALREADY_IN_ROOM},to=request.sid)
        return
    
    new_room = RoomManager(users = UserDict(userid=userid,username=sessions[userid]),
                           locked = locked,
                           password = password,
                           time_interval = time_interval)
    rooms.append(new_room)
    room_id = rooms[-1].room_id
    room_type = rooms[-1].room_type
    join_room(room_id)

    logger.info(f"Create room {room_id} by user {userid}, type is {room_type}, sid={request.sid}\n"
                +f"this room's users: {new_room.users}")
    
    avatar,_ = getSomeUserAvatar([userid])

    try:
        avatar = avatar[userid]
    except KeyError:
        avatar = None
        logger.error(f"User {userid} has no avatar")    
        
    emit('createRoomSuccess',{'room_id':room_id,'room_info':new_room.getRoomInfo(),'avatar':avatar},to=request.sid)
    # 更新sid2uid
    if request.sid not in sid2uid:
        sid2uid[request.sid] = userid

@socketio.event
@gate
def joinRoom(data):
    '''
    Description: 加入房间
    Args:
        room_id: 房间id  str
        userid: 用户id  int
        password: 房间密码 str
    Return:
        成功返回200
        room_id: 房间id  str
        userid: 用户id  int
        username: 用户名 str
    '''
    global rooms,sessions,sid2uid
    parms = {'room_id':str, 'userid':int, 'password':str}
    try:
        room_id,userid,password = getParams(parms,data, can_be_none=['password'])
    except:
        logger.error("Join room error", exc_info=True)
        emit('processWrong',{'status':PARAM_ERROR},to=request.sid)
        return
    print("params: ",room_id,userid,password)
    is_rejoin = False
    
    room = fetchRoomByRoomID(room_id,rooms)
    if room is None:
        emit('processWrong',{'status':ROOM_NOT_EXIST},to=request.sid)
        return
    # 查询该用户是否在某个房间中
    tmp_id = inWhitchRoom(userid,rooms)    
    avatar,_ = getSomeUserAvatar([userid])

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
        is_rejoin = True

    
    if room.checkPassword(password) == False:
        emit('processWrong',{'status':ROOM_PASSWORD_ERROR},to=request.sid)
        return
    
    if room.game_table and not is_rejoin:
        emit('processWrong',{'status':GAME_ALREADY_START},to=request.sid)
        return

    if room.addUser(UserDict(userid=userid,username=sessions[userid])) == False:
        emit('processWrong',{'status':ROOM_FULL},to=request.sid)
        return
    
    join_room(room_id)

    try:
        avatar = avatar[userid]
    except KeyError:
        avatar = None
        logger.error(f"User {userid} has no avatar")

    if is_rejoin:
        logger.info(f"User {userid} rejoin to game {room.game_table.game_id}"
                    +f"this room's users: {room.users}")
        emit('rejoinGameSuccess',{'room_id':room_id,'userid':userid,'username':sessions[userid],
                            'room_info':room.getRoomInfo(),'avatar':avatar},to=request.sid,namespace='/')
    else:
        logger.info(f"User {userid} join room {room_id}, sid={request.sid}"
                +f"this room's users: {room.users}")
        emit('joinRoomSuccess',{'room_id':room_id,'userid':userid,'username':sessions[userid],
                            'room_info':room.getRoomInfo(),'avatar':avatar},to=room_id)
    # 更新sid2uid
    if request.sid not in sid2uid: 
        sid2uid[request.sid] = userid

@socketio.event
@gate
def changeReadyStatus(data):
    '''
    Description: 准备游戏或取消准备
    Args:    
        room_id: 房间id str
        userid: 用户id int
    Return:
        成功返回200
    '''
    global rooms,sessions
    params = {'room_id':str, 'userid':int}
    try:
        room_id,userid = getParams(params,data)
    except:
        logger.error("Ready game error", exc_info=True)
        emit('processWrong',{'status':PARAM_ERROR},to=request.sid)
        return
    room:RoomManager = fetchRoomByRoomID(room_id,rooms)
    if room is None:
        emit('processWrong',{'status':ROOM_NOT_EXIST},to=request.sid)
        return
    room.changeReadyStatus(userid)
    emit('changeReadyStatusSuccess',{'userid':userid,'username':sessions[userid],'room_info':room.getRoomInfo()},to=room_id)
    


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
    
    if room.isHolder(userid):

        userids = [u['userid'] for u in room.users]
        emit('leaveRoomSuccess',{'userid':-1},to=room_id,namespace='/', skip_sid=request.sid)
        emit('leaveRoomSuccess',{'userid':userid,'username':sessions[userid],'room_info':room.getRoomInfo()},to=request.sid)

        for u in userids:
            sid = uid2sid(u)
            if sid: 
                leave_room(room_id,sid=sid) 
                sid2uid.pop(sid)

        rooms.remove(room)
        logger.info(f"Room {room_id} with no holder, so remove it")
    elif room.removeUser(userid):
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


@socketio.event
@gate
def removeUserFromRoom(data):
    '''
    Description: 房主移除玩家
    Args:
        room_id: 房间id str
        userid: 用户id int (房主)
        target_userid: 需要被移除的用户id int
    '''
    global rooms, sid2uid, sessions
    params = {'room_id': str, 'userid': int, 'target_userid': int}
    try:
        room_id, userid, target_userid = getParams(params, data)
    except:
        logger.error("Remove user from room error due to parameter error", exc_info=True)
        emit('processWrong', {'status': PARAM_ERROR}, to=request.sid)
        return

    # 获取房间对象
    room: RoomManager = fetchRoomByRoomID(room_id, rooms)
    if room is None:
        logger.error(f"No such room {room_id}")
        emit('processWrong', {'status': ROOM_NOT_EXIST}, to=request.sid)
        return

    # 检查提出请求的用户是否是房主
    if not room.isHolder(userid):
        logger.error(f"User {userid} is not the holder of room {room_id}")
        emit('processWrong', {'status': NOT_HOLDER}, to=request.sid)
        return

    # 检查需要移除的目标用户是否是房主
    if room.isHolder(target_userid):
        logger.error(f"Failed to remove user {target_userid} from room {room_id} because User {target_userid} is the holder of room {room_id}")
        emit('processWrong', {'status': REMOVE_USER_FAILED}, to=request.sid)
        return

    # 从房间中移除目标用户
    if room.removeUser(target_userid):
        emit('userRemovedSuccess', {'userid': target_userid, 'username': sessions[target_userid], 'room_info': room.getRoomInfo()}, to=room_id)
        sid = uid2sid(target_userid)
        if sid:
            leave_room(room_id, sid=sid)
            if sid in sid2uid:
                sid2uid.pop(sid)
        logger.info(f"User {target_userid} removed from room {room_id} by holder {userid}")

        # 房间为空, 移除房间
        # if len(room.users) == 0:
        #     rooms.remove(room)
        #     close_room(room=room_id,namespace='/')
        #     logger.info(f"Room {room_id} is empty, remove it")
    else:
        logger.error("User {0} not in room {1}".format(userid,room_id))
        emit('processWrong',{'status':NOT_IN_ROOM},to=request.sid)


@app.route('/api/game/create', methods=['POST'])
@gate
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
        if room.isAllReady() == False:
            emit('processWrong',{'status':NOT_ALL_READY},to=uid2sid(userid),namespace='/')
            return "{message: '房间未准备好！'}",NOT_ALL_READY

        game:GameTable = GameTable(room.users[:3], 
                                   room.users[3:] if len(room.users) > 3 else [],
                                   room.time_interval)
        
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

    return jsonify({'game_info':game.getGameInfo(),'next_time':game.next_time}),SUCCESS


@socketio.event
@gate
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
                                     'x2':x2, 'y2':y2, 'z2':z2,'next_time':game.next_time},
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
    logger.info(f"EndRankGame")
    # 游戏结束，判断胜利者或平局
    logger.debug("game end")
    if room_type == 2:
        endRankGame(game)
    if game.game_state == EnumGameState.win:
        # 记录结束时间
        game.record.end_time = datetime.datetime.now()
        # 通知所有玩家游戏结束并告知胜利者
        logger.info(f"Game {game.game_id} end, winner is {sessions[userid] if userid in sessions else 'None'}")
        print(game.record.end_time)
        print(game.record.start_time)
        match_duration = (game.record.end_time - game.record.start_time)
        print(f"对局时长为：{match_duration}")
        # 结束记录
        state,record_id = game.record.recordEnd(userid)
        emit('gameEnd', {'status': GAME_END, 'record_id':record_id, 'room_info':room.getRoomInfo(),'room_type':room_type,"step_count":game.step_count,"match_duration": match_duration.total_seconds(),'winner': userid, 'winner_name': sessions[userid]}, to=room.room_id, namespace='/')

    elif game.game_state == EnumGameState.draw:
        # 记录结束时间
        game.record.end_time = datetime.datetime.now()
        # 通知所有玩家游戏结束为平局
        logger.info(f"Game {game.game_id} end, winner is {sessions[userid] if userid in sessions else 'None'}")
        match_duration = (game.record.end_time - game.record.start_time)
        # 结束记录
        state,recordId=game.record.recordEnd(None)
        emit('gameEnd', {'status': GAME_END, 'recordId':recordId,'room_type':room_type,"step_count":game.step_count,"match_duration": match_duration.total_seconds(),'winner': -1, 'winner_name': None}, to=room.room_id,namespace='/')

    room.removeGameTable()
    if room.room_type == RoomType.matched:
        try:
            logger.info(f"Remove room {room.room_id} after game end")
            rooms.remove(room)
            close_room(room=room.room_id,namespace='/')
        except Exception as e:
            logger.error("May remove in other way. Remove room error due to {0}".format(str(e)), exc_info=True)

@socketio.event
@gate
def watchGame(data):
    """
    请求观战，前提是游戏已经开始
    Args:
        userid: 用户id          int
        room_id: 房间id        str
        password: 房间密码      str
    """
    global rooms
    params = {'userid':int,  'room_id':str, 'password':str}
    try:
        userid,room_id,password = getParams(params,data,can_be_none=['password'])
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
        if room.checkPassword(password) == False:
            emit('processWrong',{'status':ROOM_PASSWORD_ERROR},to=request.sid)
            return
        if room.game_table.addViewer(user):
            room.addUser(user)
            join_room(room_id)
            logger.info(f"User {userid} watch game {room.game_table.game_id} and join room {room_id}")
            # 需要前端根据自己的身份来决定是成功加入观战，还是某某进入观战
            emit('watchGameSuccess',{'room_info':room.getRoomInfo(),'game_info':room.game_table.getGameInfo()},to=room_id,namespace='/')
        else:
            emit('processWrong',{'status':NOT_JOIN_GAME},to=request.sid)
    except Exception as e:
        logger.error("Watch game error due to {0}".format(str(e)), exc_info=True)
        emit('processWrong',{'status':OTHER_ERROR},to=request.sid)
        return

        

@socketio.event
@gate
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
        emit('surrenderSuccess',{'userid':userid,'username':sessions[userid],
                                'game_info':game.getGameInfo(),'next_time':game.next_time},to=room_id)
        # 判断游戏是否结束
        if status == GAME_END:
            roomOver(game=game, room=room, userid=game.winner_id)
        
    except Exception as e:
        logger.error("Request surrender error due to {0}".format(str(e)), exc_info=True)
        emit('processWrong',{'status':OTHER_ERROR},to=request.sid)


@socketio.event
@gate
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
    
    room_id = inWhitchRoom(userid,rooms)
    if room_id is None:
        emit('processWrong',{'status':NOT_IN_ROOM},to=request.sid)
        return
    game:GameTable = fetchRoomByRoomID(room_id,rooms).game_table
    if game is None:
        emit('processWrong',{'status':NOT_JOIN_GAME},to=request.sid)
        return
    try:
        if game.requestDraw(userid):
        # 广播求和请求给其他存活的玩家
            emit('drawRequest', {'requester': userid, 'username': sessions[userid]}, to=room_id, skip_sid=request.sid)
        else:
            emit('processWrong',{'status':REPEAT_DRAW_REQUEST},to=request.sid)
        return
    except Exception as e:
        logger.error("Request draw error due to {0}".format(str(e)), exc_info=True)
        emit('processWrong',{'status':OTHER_ERROR},to=request.sid)
        return 
    
@socketio.event
@gate
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
    room = fetchRoomByRoomID(room_id,rooms)
    game = room.game_table
    if game is None:
        emit('processWrong',{'status':NOT_JOIN_GAME},to=request.sid)
        return
    try:
        game.respondDraw(userid, agree)
        # 所有存活的玩家均已回应
        if len(game.draw_respondents) == len(game.getAlivePlayers()):
            for res_agree in game.draw_agree:
                if res_agree == False:
                    logger.info(f"Draw was rejected, so game continues")
                    emit('gameOngoing', {'status': SUCCESS,'userid': userid, 'username': sessions[userid]}, to=room_id)
                    game.setDraw(False)
                    return

            game.setDraw(True)

            roomOver(game=game, room=room, userid=game.winner_id)
        else:
            emit('waitForOthers', {'status': SUCCESS, 'userid': userid, 'username': sessions[userid], 'agree': agree}, to=room_id)
        return
    except Exception as e:
        logger.error("Respond draw error due to {0}".format(str(e)), exc_info=True)
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
                    room = RoomManager(users=[UserDict(userid=user0,username=sessions[user0]),
                                              UserDict(userid=user1,username=sessions[user1]),
                                              UserDict(userid=user2,username=sessions[user2])],
                                        room_type=RoomType.matched)
                    rooms.append(room)
                    
                    room.game_table = GameTable(room.users)

                    for user in room.users:
                        join_room(room=room.room_id,sid=uid2sid(user['userid']),namespace='/')

                    logger.info(f"Create room : {room.room_id} and game: {room.game_table.game_id}"
                                + f" with users: {user0}, {user1}, {user2}")
                    # 通知房间所有人匹配到了
                    emit('startMatchSuccess',{'game_id':room.game_table.game_id,
                                            'room_info':room.getRoomInfo()},
                                            to=room.room_id,namespace='/')
                except Exception as e:
                    logger.error("Create match_game error due to {0}".format(str(e)), exc_info=True)
                    for user in [user0,user1,user2]:
                        if user and user in sessions:
                            match_queue.put(user)

            time.sleep(1)

def cycleRank(app):
    """
    排位模式下，定时检查的守护进程，检查是否有玩家加入排位队列，若有则创建房间
    """
    global rooms, rank_queue, sessions, rank_table
    with app.app_context():
        while True:

            if rank_queue.qsize() >= 3:
                user_list = []
                for _ in range(rank_queue.qsize()):
                    user_list.append(rank_queue.get())
                
                eligible_users = []
                # 将段位符合的[user1，user2]组加入到eligible_users中
                for i, user1 in enumerate(user_list):
                    for j, user2 in enumerate(user_list[i+1:], start=i+1):
                        if user1 != user2 and isEligible(*rank_table[user1], *rank_table[user2]):
                            eligible_users.append([user1, user2])

                # 再遍历user_list，将各个user与eligible_users中的各组中的两个user分别进行比对
                # 第一组段位符合的 3 个玩家进行匹配
                matched_users = None
                for [user1, user2] in eligible_users:
                    for user in user_list:
                        if user != user1 and user != user2 and isEligible(*rank_table[user], *rank_table[user1]) and isEligible(*rank_table[user], *rank_table[user2]):
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
                        room = RoomManager(users=[UserDict(userid=user0, username=sessions[user0]),
                                            UserDict(userid=user1, username=sessions[user1]),
                                            UserDict(userid=user2, username=sessions[user2])], 
                                            room_type=RoomType.ranked)
                        rooms.append(room)
                        room.game_table = GameTable(room.users)
                        for user in room.users:
                            join_room(room=room.room_id, sid=uid2sid(user['userid']),namespace='/')
                        logger.info(f"Create room : {room.room_id} and game: {room.game_table.game_id}"
                                    + f" with users: {user0}, {user1}, {user2}")
                        # 通知房间所有人匹配到了，并展示各玩家段位和积分
                        emit('startRankSuccess',{'game_id':room.game_table.game_id,
                                            'room_info':room.getRoomInfo(),
                                            'ranks': [rank_table[user0][0], rank_table[user1][0], rank_table[user2][0]],
                                            'scores': [rank_table[user0][1], rank_table[user1][1], rank_table[user2][1]]},
                                            to=room.room_id,namespace='/')
                    except Exception as e:
                        logger.error("Create rank_game error due to {0}".format(str(e)), exc_info=True)
                        # 重新将所有用户放回队列
                        for user in user_list:
                            if user and user in sessions:
                                rank_queue.put(user)

                else:
                    # 重新将所有用户放回队列
                    for user in user_list:
                        if user and user in sessions:
                            rank_queue.put(user)

            time.sleep(1)

def cycleTimeout(app):
    """
    定时检查走棋超时的守护进程
    """
    global rooms,sessions,timeout_heap
    with app.app_context():
        while True:
            while True:
                try:
                    next = heapq.heappop(timeout_heap)
                    if next[0] > time.time():
                        heapq.heappush(timeout_heap,next)
                        logger.info(f"User {userid} left time {next[0] - time.time()}")
                        break
                except Exception as e:
                    break
                userid = next[1]
                room_id = inWhichGame(userid,rooms)
                if room_id is None:
                    continue
                room:RoomManager = fetchRoomByRoomID(room_id,rooms)
                if room is None:
                    logger.info(f"room id {room_id} not exist")
                    continue
                
                game_table:GameTable = room.game_table
                if game_table is None:
                    logger.info(f"room id {room_id} has no game")
                    continue
                if game_table.next_time > next[0]:
                    logger.info(f"next time {next[0]} satisfied")
                    continue
                try:
                    # 玩家投降
                    status = game_table.surrender(userid)
                    logger.info(f"User {userid} timeout")
                    # 通知所有玩家有玩家超时
                    emit('surrenderTimeout',{'userid':userid,'username':sessions[userid],
                                            'game_info':game_table.getGameInfo(),'next_time':game_table.next_time},
                        namespace='/' , to=room_id)
                    # 判断游戏是否结束
                    if status == GAME_END:
                        roomOver(game=game_table, room=room, userid=game_table.winner_id)
                    
                except Exception as e:
                    logger.error("Request surrender error due to {0}".format(str(e)), exc_info=True)
                    emit('processWrong',{'status':OTHER_ERROR},to=request.sid)
                    
            time.sleep(1)

@socketio.event
@gate
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
@gate
def startRank(data):
    """
    接收玩家开始排位匹配请求
    Args:
        userid: 用户id      int 
    """
    global rooms, rank_queue ,rank_table
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
    
    user_rank, user_score = result
    sid2uid[request.sid] = userid # 维护sid2uid映射

    # rank_queue.put((userid, user_rank, user_score)) 一把拍死这样写的
    rank_queue.put(userid)
    rank_table[userid] = (user_rank, user_score)

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
        if userid == -1:
            records,status = viewAllVisibleGameRecords()
            logger.info('view all game records num={}'.format(len(records)))
        else:
            records,status = viewUserGameRecords(userid)
        if status == SUCCESS:
            emit('gameRecord', {'record': records}, to=request.sid)
        else:
            emit('processWrong',{'status':status},to=request.sid)
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

@app.route('/api/changeVisible', methods=['POST'])
def changeVisibleApi():
    """
    修改游戏记录可见性请求
    Args:
        record_id: 对局id      int 
        visible:   是否可见    int
    """
    params = {'record_id':int,'visible':int}
    try:
        record_id,visible = getParams(params,request.form)
    except:        
        return '{}',PARAM_ERROR
    try:
        # 修改游戏记录可见性
        return changeGameRecordVisible(record_id,visible)
    except Exception as e:
        logger.error("failed to change game record visible due to {0}".format(str(e)), exc_info=True)
        return '{}',OTHER_ERROR

@socketio.event
def sendMessage(data):
    """_summary_

    Args:
        data (_type_): _description_
    """
    global sessions
    params = {'message':str,'userid':int}
    try:
        message,userid = getParams(params,data)
    except:
        emit('processWrong',{'status':PARAM_ERROR},to=request.sid)
        return
    room_id = inWhitchRoom(userid,rooms)

    emit('receiveMessage',{'username':sessions[userid],'message':message,'userid':userid},to=room_id,
            skip_sid=request.sid)
    

def subtractSesion():
    """
    定时清理过期session
    """
    global sessions,session_times
    while True:
        li = list(sessions.keys())
        for key in li:
            try:
                if time.time() - session_times[key] > 60*60*1:  # 1小时
                    sessions.pop(key)
                    session_times.pop(key)
            except Exception as e:
                logger.error("Failed to delete session due to {0}".format(str(e)), exc_info=True)
        time.sleep(60*5)


def viewQueue():
    # bebug
    global match_queue,rank_queue
    while True:
        input()
        print(f"match_queue size: {match_queue.qsize()}, rank_queue size: {rank_queue.qsize()}")
        print(f"match_queue: {match_queue.queue}, rank_queue: {rank_queue.queue}")
        print(f'match_set: {match_queue.queue_set}, rank_set: {rank_queue.queue_set}')

def surrenderGame(game:GameTable, userid:int):
    """
    投降游戏
    Args:
        game: 游戏对象
        userid: 投降用户id
    """
    game.surrender(userid)
    return SUCCESS

threading.Thread(target=subtractSesion,daemon=True, name='subtractSesion').start()
threading.Thread(target=cycleMatch,args=[app] ,daemon=True, name='cycleMatch').start()  #bug uwsgi不执行main函数
threading.Thread(target=cycleRank,args=[app] ,daemon=True, name='cycleRank').start()
threading.Thread(target=cycleTimeout,args=[app] ,daemon=True, name='cycleTimeout').start()
# threading.Thread(target=viewQueue,daemon=True, name='viewQueue').start()

if __name__ == "__main__":
    socketio.run(app,debug=True,host='0.0.0.0',port=8888,allow_unsafe_werkzeug=True)
    print("Good bye!")