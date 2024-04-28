import os
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.absolute()
os.environ['PROJECT_ROOT'] = str(project_root)
sys.path.append(str(Path(__file__).resolve().parent.parent))
print("Project root set to:", os.environ['PROJECT_ROOT']) # 设置项目根目录

import flask
from flask_cors import CORS
from flask import request
from log_tool import setupLogger 
from user_manage import login, register
from game.exception import *
from message import *
from game import GameTable, fetchGameByUserID

app = flask.Flask(__name__)
CORS(app, resources=r'/*')

# 日志工具
logger = setupLogger()

games:list[GameTable] = []

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

@app.route('/api/game/create', methods=['POST'])
def createGameApi():
    '''
    Args:
        user1id: 用户1id
        user2id: 用户2id
        user3id: 用户3id
    Returns:
        创建成功200
    '''
    try:
        user1id = request.form.get('user1id')
        user2id = request.form.get('user2id')
        user3id = request.form.get('user3id')
    except:
        return "{message: 'parameter error'}",PARAM_ERROR
    try:
        game = GameTable(user1id, user2id, user3id)
        games.append(game)
        logger.info("Create game: {0}".format(game.game_id))
    except:
        logger.error("Create game error", exc_info=True)
        return "{message: 'create game error'}",GAME_CREATE_FAILED


@app.route('/api/game/move', methods=['POST'])
def moveApi():
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
        userid = request.form.get('userid')
        chess_type = request.form.get('chess_type')
        x1 = request.form.get('x1')
        y1 = request.form.get('y1')
        z1 = request.form.get('z1') 
        x2 = request.form.get('x2')
        y2 = request.form.get('y2')
        z2 = request.form.get('z2')
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

if __name__ == "__main__":

    app.run(host='0.0.0.0',port=8888)

    print("Good bye!")