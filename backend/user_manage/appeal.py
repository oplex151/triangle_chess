from enum import Enum
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


class AppealType(Enum):
    report = 0
    normal = 1

def addAppeals(userid, appeal_type, content, fromid):
    db = pymysql.connect(host="127.0.0.1",user="root",password=password,database=DATA_BASE)
    cursor = db.cursor()
    # 插入申诉信息到数据库
    try:
        insert_query = "INSERT INTO {0} (userId, type, content, fromId) VALUES (%s, %s, %s, %s);".format(APPEAL_TABLE)
        cursor.execute(insert_query, (userid, appeal_type, content, fromid))
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

def getAppeals(userid=None):    
    db = pymysql.connect(host="127.0.0.1",user="root",password=password,database=DATA_BASE)
    cursor = db.cursor()
    # 查询数据库中某个用户的申诉
    try:
        db.begin()
        cursor.connection.ping(reconnect=True) 
        if userid is None:
            select_query = "SELECT * FROM {0};".format(APPEAL_TABLE)
            cursor.execute(select_query)
        else:
            select_query = "SELECT * FROM {0} WHERE fromId = %s;".format(APPEAL_TABLE)
            cursor.execute(select_query, (userid))
        appeals = cursor.fetchall() 
    except Exception as e:
        logger.error(e,exc_info=True)
    finally:
        cursor.close()
        db.close()
    return appeals if appeals else None

def getAppealsInfo(userid):
    db = pymysql.connect(host="127.0.0.1",user="root",password=password,database=DATA_BASE)
    cursor = db.cursor()
    res = {}
    try:
        appeals = getAppeals(userid) # 获取申诉信息
        if not appeals:
            return "{}",NO_APPEALS
        res = []
        for appeal in appeals:
            appealid, userid, appeal_type, content, timestamp, fromid, dealed, feedback = appeal
            sql =(f"SELECT userName FROM {USER_TABLE} WHERE userId = {userid}") # sql可以优化
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                username = result[0]
                res.append({"appealid":appealid,
                            "userid":userid,
                            "username":username,
                            "type":appeal_type,
                            "timestamp":timestamp,
                            "content":content,
                            "fromid":fromid,
                            "dealed":dealed,
                            "feedback":feedback if dealed else ""})
        logger.debug(res)
        status = SUCCESS
    except Exception as e:
        logger.error(e)
        status = OTHER_ERROR
    finally:
        cursor.close()
        db.close()
    return jsonify(res),status

def handleAppeal(appealid, feedback):
    db = pymysql.connect(host="127.0.0.1",user="root",password=password,database=DATA_BASE)
    cursor = db.cursor()
    try:
        update_query = "UPDATE {0} SET dealed = 1, feedback = %s WHERE appealId = %s;".format(APPEAL_TABLE)
        cursor.execute(update_query, (feedback, appealid))
        db.commit()
        status = SUCCESS
    except Exception as e:
        logger.error(e)
        status = OTHER_ERROR
    finally:
        cursor.close()
        db.close()
    return "{}",status