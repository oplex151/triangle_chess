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
def register(username, password, email, phone_num, gender):
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
            insert_query =  "".join([f"INSERT INTO {USER_TABLE} (userName, ",
            f"{'gender, ' if gender else ''}",
            f"{'phoneNum, ' if phone_num else ''}",
            f"{'email, ' if email else ''}",
            f"userPassword) VALUES (",
            f"'{username}', ",
            f'\'{gender}\', ' if gender else '' ,
            f'\'{phone_num}\', ' if phone_num else '',
            f'\'{email}\', ' if email else '',
            f"'{password}'",
            ");"])   # 一个句子写哭我
            print(insert_query)
            try:
                cursor.execute(insert_query)
            except Exception as e:
                db.rollback()
                logger.error("User {0} failed to register for {1}".format(username,str(e)))
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

@connectDatabase
def changeUserInfo(userid:int, username:str=None, email:str=None, phone_num:str=None, gender:str=None):
    res,status = {},None
    try:
        # 首先就检查用户名是否已经存在
        db.begin()
        select_query = "SELECT * FROM {0} WHERE userId = {1};".format(USER_TABLE, userid)
        cursor.execute(select_query)
        data = cursor.fetchone()
        if data is None:
            logger.error("User {0} not exists".format(userid))
            return None,USER_NOT_EXIST
        if username is not None:
            # 先看看用户名是否已经存在
            select_query = "SELECT * FROM {0} WHERE userName = {1};".format(USER_TABLE,"'"+username+"'")
            cursor.execute(select_query)
            result = cursor.fetchone()
            if result is not None and result[0] != data[0]:
                logger.error("UserName {0} already exists".format(username))
                status = NAME_ALREADY_EXIST
                raise Exception("UserName already exists")
            else:
                update_query = "UPDATE {0} SET userName = {1} WHERE userId = {2};".format(USER_TABLE,"'"+username+"'",userid)
                cursor.execute(update_query)
        if email is not None:
            update_query = "UPDATE {0} SET email = {1} WHERE userId = {2};".format(USER_TABLE,"'"+email+"'",userid)
            cursor.execute(update_query)
        if phone_num is not None:
            update_query = "UPDATE {0} SET phoneNum = {1} WHERE userId = {2};".format(USER_TABLE,"'"+phone_num+"'",userid)
            cursor.execute(update_query)
        if gender is not None:
            update_query = "UPDATE {0} SET gender = {1} WHERE userId = {2};".format(USER_TABLE,"'"+gender+"'",userid)
            cursor.execute(update_query)
        db.commit()
        logger.info("User {0} changed user info successfully".format(userid))
        status = SUCCESS
    except Exception as e:
        logger.error("User {0} failed to change user info due to\n{1}".format(userid,str(e)),exc_info=True)
        status = OTHER_ERROR if status is None else status
    finally:
        cursor.close()
        db.close()
    return jsonify(res),status

@connectDatabase
def changePassword(userid:int, old_password:str, new_password:str):
    res,status = {},None
    try:
        # 首先就检查用户名是否已经存在
        db.begin()
        select_query = "SELECT userPassword FROM {0} WHERE userId = {1};".format(USER_TABLE, userid)
        cursor.execute(select_query)
        data = cursor.fetchone()
        if data is None:
            logger.error("User {0} not exists".format(userid))
            status = USER_NOT_EXIST
            raise Exception("User not exists")
        if data[0] != old_password:
            logger.error("User {0} failed to change password due to wrong old password".format(userid))
            status = WRONG_OLD_PASSWORD
            raise Exception("Wrong old password")
        else:
            update_query = "UPDATE {0} SET userPassword = {1} WHERE userId = {2};".format(USER_TABLE,"'"+new_password+"'",userid)
            cursor.execute(update_query)
        db.commit()
        logger.info("User {0} changed password successfully".format(userid))
        status = SUCCESS
    except Exception as e:
        logger.error("User {0} failed to change password due to\n{1}".format(userid,str(e)),exc_info=True)
        status = OTHER_ERROR if status is None else status
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