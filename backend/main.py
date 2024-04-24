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
from backend.user_manage import login, register
from game.exception import *
from message import *

app = flask.Flask(__name__)
CORS(app, resources=r'/*')

# 日志工具
logger = setupLogger()

@app.route('/login', methods=['POST'])
def loginApi():
    '''
    Args:
        username: 用户名
        password: 密码
    Returns:
        登录成功200
    '''
    username = request.form.get('username')
    password = request.form.get('password')
    return login(username, password)

@app.route('/register', methods=['POST'])
def registerApi():
    '''
    Args:
        username: 用户名
        password: 密码
    Returns:
        注册成功200
    '''
    username = request.form.get('username')
    password = request.form.get('password')
    return register(username, password)

@app.route('/game/move', methods=['POST'])
def moveApi():
    '''
    Args:
        username: 用户名
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
    username = request.form.get('username')
    chess_type = request.form.get('chess_type')
    x1 = request.form.get('x1')
    y1 = request.form.get('y1')
    z1 = request.form.get('z1') 
    x2 = request.form.get('x2')
    y2 = request.form.get('y2')
    z2 = request.form.get('z2')
    pass


if __name__ == "__main__":

    app.run(host='0.0.0.0',port=8888)

    print("Good bye!")