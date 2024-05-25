from functools import wraps
import os
import pymysql
from dotenv import load_dotenv
from flask import jsonify
from backend.tools import setupLogger
from backend.message import *
from backend.global_var import rooms,sessions

DATA_BASE = "trianglechess" # 数据库名称
USER_TABLE = "user"

load_dotenv()
password = os.getenv("MYSQL_PASSWORD")

db = None
cursor = None

logger = setupLogger()


def connectDatabase(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        global db, cursor
        db = pymysql.connect(host="127.0.0.1",user="root",password=password,database=DATA_BASE)
        cursor = db.cursor()
        return func(*args, **kwargs)
    return wrapper

@connectDatabase
def login(username, password):
    global sessions
    res,status = {},None
    try:
        db.begin()
        select_query = "SELECT userPassword, userId FROM {0} WHERE userName = {1};".format(USER_TABLE,"'"+username+"'")
        cursor.execute(select_query)
        result = cursor.fetchone()
        if result is not None and result[0] == password:
            if result[1] in sessions:
                logger.error("User {0} already logged in".format(username))
                return "{}",ALREADY_LOGIN
            logger.info("User {0} logged in successfully usring id {1}".format(username,result[1]))
            res = {"userid":result[1]}
            sessions[result[1]] = username
            status = SUCCESS
        elif result is not None and result[0] != password:
            logger.error("User {0} failed to login due to wrong password".format(username))
            status = LOGIN_WRONG_PASSWORD
        else:
            logger.error("User {0} does not exist".format(username))
            status = LOGIN_UNEXIST_USER
    except Exception as e:
        logger.error("User {0} failed to login due to\n{1}".format(username,str(e)))
        status = OTHER_ERROR
    finally:
        cursor.close()
        db.close()
    return jsonify(res),status
    
@connectDatabase
def register(username, password):
    res,status = {},None
    try:
        # 首先就检查用户名是否已经存在
        db.begin()
        select_query = "SELECT * FROM {0} WHERE userName = {1};".format(USER_TABLE,"'"+username+"'")
        cursor.execute(select_query)
        result = cursor.fetchone()
        if result is not None:
            logger.error("User {0} already exists".format(username))
            status = REGISTER_EXIST_USER
        else:
            insert_query = "INSERT INTO {0} (userName, userPassword) VALUES ({1}, {2});".format(USER_TABLE,"'"+username+"'", "'"+password+"'")
            try:
                cursor.execute(insert_query)
            except:
                db.rollback()
                logger.error("User {0} failed to register".format(username))
                status = REGISTER_FAILED
            else:
                db.commit()
                logger.info("User {0} registered successfully".format(username))
                status = SUCCESS
    except Exception as e:
        logger.error("User {0} failed to register due to\n{1}".format(username,str(e)))
        status = OTHER_ERROR
    finally:
        cursor.close()
        db.close()
    return jsonify(res),status
    
def logout(userid:int):
    global sessions
    if userid in sessions.keys(): 
        sessions.pop(userid)
        logger.info("User {0} logged out successfully".format(userid))
        return "{}",SUCCESS
    else:
        logger.error("User {0} not logged in".format(userid))
        return "{}",USER_NOT_LOGIN

@connectDatabase
def getUserInfo(userid:int):
    dic, status = {}, None
    try:
        # 首先就检查用户名是否已经存在
        db.begin()
        select_query = "SELECT * FROM {0} WHERE userId = {1};".format(USER_TABLE, userid)
        cursor.execute(select_query)
        data = cursor.fetchone()
        if data is None:
            logger.error("User {0} not exists".format(userid))
            return None,USER_NOT_EXIST
        dic["userId"] = data[0]
        dic["userName"] = data[1]
        dic['rank'] = data[3]
        dic['score'] = data[4]
        dic['gender'] = data[5]
        dic['phoneNum'] = data[6]
        dic['email'] = data[7]
        status = SUCCESS
    except Exception as e:
        logger.error("User {0} failed to get user info due to\n{1}".format(userid,str(e)),exc_info=True)
        status = OTHER_ERROR
    finally:
        cursor.close()
        db.close()
    return jsonify(dic),status