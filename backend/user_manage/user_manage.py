import os
import pymysql
from dotenv import load_dotenv
from flask import jsonify
from backend.log_tool import setupLogger
from backend.message import *

DATA_BASE = "TriangleChess"
USER_TABLE = "user"

load_dotenv()
password = os.getenv("MYSQL_PASSWORD")

db = pymysql.connect(host="127.0.0.1",user="root",password=password,database=DATA_BASE)
cursor = db.cursor()

logger = setupLogger()

def login(username, password):
    try:
        select_query = "SELECT Password, UserID FROM {0} WHERE UserName = {1};".format(USER_TABLE,"'"+username+"'")
        cursor.execute(select_query)
        result = cursor.fetchone()
        if result is not None and result[0] == password:
            logger.info("User {0} logged in successfully".format(username))
            res = {"userid":result[1]}
            return jsonify(res),SUCCESS
        elif result[0] != password:
            logger.error("User {0} does not exist".format(username))
            return "{}",LOGIN_WRONG_PASSWORD
        else:
            logger.error("User {0} failed to login".format(username))
            return "{}",LOGIN_UNEXIST_USER
    except Exception as e:
        logger.error("User {0} failed to login due to\n{1}".format(username,str(e)))
        return "{}",OTHER_ERROR
    
def register(username, password):
    try:
        # 首先就检查用户名是否已经存在
        select_query = "SELECT * FROM {0} WHERE UserName = {1};".format(USER_TABLE,"'"+username+"'")
        cursor.execute(select_query)
        result = cursor.fetchone()
        if result is not None:
            logger.error("User {0} already exists".format(username))
            return "{}",REGISTER_EXIST_USER
        else:
            # TODO:为用户生成ID
            insert_query = "INSERT INTO {0} (UserName, Password) VALUES ({1}, {2});".format(USER_TABLE,"'"+username+"'", "'"+password+"'")
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