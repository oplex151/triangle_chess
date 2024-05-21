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

db = pymysql.connect(host="127.0.0.1",user="root",password=password,database=DATA_BASE)
cursor = db.cursor()

logger = setupLogger()

def login(username, password):
    global sessions
    try:
        select_query = "SELECT userPassword, userId FROM {0} WHERE UserName = {1};".format(USER_TABLE,"'"+username+"'")
        cursor.execute(select_query)
        result = cursor.fetchone()
        if result is not None and result[0] == password:
            if result[1] in sessions:
                logger.error("User {0} already logged in".format(username))
                return "{}",ALREADY_LOGIN
            logger.info("User {0} logged in successfully usring id {1}".format(username,result[1]))
            res = {"userid":result[1]}
            sessions[result[1]] = username
            return jsonify(res),SUCCESS
        elif result is not None and result[0] != password:
            logger.error("User {0} failed to login due to wrong password".format(username))
            return "{}",LOGIN_WRONG_PASSWORD
        else:
            logger.error("User {0} does not exist".format(username))
            return "{}",LOGIN_UNEXIST_USER
    except Exception as e:
        logger.error("User {0} failed to login due to\n{1}".format(username,str(e)))
        return "{}",OTHER_ERROR
    
def register(username, password):
    try:
        # 首先就检查用户名是否已经存在
        select_query = "SELECT * FROM {0} WHERE userName = {1};".format(USER_TABLE,"'"+username+"'")
        cursor.execute(select_query)
        result = cursor.fetchone()
        if result is not None:
            logger.error("User {0} already exists".format(username))
            return "{}",REGISTER_EXIST_USER
        else:
            insert_query = "INSERT INTO {0} (userName, userPassword) VALUES ({1}, {2});".format(USER_TABLE,"'"+username+"'", "'"+password+"'")
            try:
                cursor.execute(insert_query)
                db.commit()
                logger.info("User {0} registered successfully".format(username))
                return "{}",SUCCESS
            except:
                db.rollback()
                logger.error("User {0} failed to register".format(username))
                return "{}",REGISTER_FAILED
    except Exception as e:
        logger.error("User {0} failed to register due to\n{1}".format(username,str(e)))
        return "{}",OTHER_ERROR
    
def logout(userid:int):

    global sessions
    if userid in sessions.keys(): 
        sessions.pop(userid)
        logger.info("User {0} logged out successfully".format(userid))
        return "{}",SUCCESS
    else:
        logger.error("User {0} not logged in".format(userid))
        return "{}",USER_NOT_LOGIN
    
def viewUserRank(userid:int):
    try:
        # 首先就检查用户名是否已经存在
        select_query = "SELECT `rank`, score FROM {0} WHERE userId = {1};".format(USER_TABLE, userid)
        cursor.execute(select_query)
        result = cursor.fetchone()
        if result is None:
            logger.error("User {0} not exists".format(userid))
            return None
        return result
    except Exception as e:
        logger.error("User {0} failed to view rank due to\n{1}".format(userid,str(e)))
        return None
    
def getUserInfo(userid:int):
    try:
        # 首先就检查用户名是否已经存在
        select_query = "SELECT * FROM {0} WHERE userId = {1};".format(USER_TABLE, userid)
        cursor.execute(select_query)
        data = cursor.fetchone()
        if data is None:
            logger.error("User {0} not exists".format(userid))
            return None,USER_NOT_EXIST
        dic = {}
        dic["userId"] = data[0]
        dic["userName"] = data[1]
        dic['rank'] = data[3]
        dic['score'] = data[4]
        dic['gender'] = data[5]
        dic['phoneNum'] = data[6]
        dic['email'] = data[7]
        return jsonify(dic),SUCCESS
    except Exception as e:
        logger.error("User {0} failed to get user info due to\n{1}".format(userid,str(e)),exc_info=True)
        return None,OTHER_ERROR