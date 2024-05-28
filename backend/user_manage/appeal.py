import os
import pymysql
from dotenv import load_dotenv
from flask import jsonify
from backend.tools import setupLogger
from backend.message import *
from backend.global_var import rooms,sessions

DATA_BASE = "trianglechess" # 数据库名称
USER_TABLE = "user"
APPEAL_TABLE = "appeal"

load_dotenv()
password = os.getenv("MYSQL_PASSWORD")

logger = setupLogger()

def addAppeals(userid, appeal_type, content):
    db = pymysql.connect(host="127.0.0.1",user="root",password=password,database=DATA_BASE)
    cursor = db.cursor()
    # 插入申诉信息到数据库
    try:
        insert_query = "INSERT INTO {0} (userid, type, content) VALUES (%s, %s, %s);".format(APPEAL_TABLE)
        cursor.execute(insert_query, (userid, appeal_type, content))
    except Exception as e:
        db.rollback()
        logger.error("add appeal error: "+str(e))
        status = OTHER_ERROR
    else:
        db.commit()
        status = SUCCESS
    finally:
        cursor.close()
        db.close()
    return "{}",status

def isAdmin(adminid):
    # 检查是否是管理员用户
    # 暂设只有userid小于10是管理员
    return adminid < 10

def getAppeals(userid):    
    db = pymysql.connect(host="127.0.0.1",user="root",password=password,database=DATA_BASE)
    cursor = db.cursor()
    # 查询数据库中某个用户的申诉
    try:
        db.begin()
        cursor.connection.ping(reconnect=True) 
        select_query = "SELECT userId, type, content FROM {0} WHERE userId = %s;".format(APPEAL_TABLE)
        cursor.execute(select_query, (userid))
        appeals = cursor.fetchall() 
    except Exception as e:
        logger.error(e,exc_info=True)
    finally:
        cursor.close()
        db.close()
    return appeals if appeals else None

def getAppealsInfo(userid, adminid):
    # 检查是否是管理员用户
    if isAdmin(adminid) is False:
        return "{}", NOT_ADMIN
    
    db = pymysql.connect(host="127.0.0.1",user="root",password=password,database=DATA_BASE)
    cursor = db.cursor()
    result = {}
    try:
        # 获取用户的好友列表
        logger.debug(userid)
        appeals = getAppeals(userid)
        if not appeals:
            return "{}",NO_APPEALS
        appeals_info = []
        for appeal in appeals:
            userid, appeal_type, content = appeal
            sql =(f"SELECT userName FROM {USER_TABLE} WHERE userId = {userid}") # sql可以优化
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                username = result[0]
                appeals_info.append({"userid":userid,"username":username,"type":appeal_type,"content":content})
        logger.debug(appeals_info)
        result = {'appeals':appeals_info}
        status = SUCCESS
    except Exception as e:
        logger.error(e)
        status = OTHER_ERROR
    finally:
        cursor.close()
        db.close()
    return jsonify(result),status