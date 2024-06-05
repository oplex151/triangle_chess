import os
import pymysql
from dotenv import load_dotenv
from flask import jsonify
from backend.tools import setupLogger
from backend.message import *
from backend.global_var import rooms,sessions

DATA_BASE = "trianglechess" # 数据库名称
USER_TABLE = "user"
FRIEND_TABLE = "friend"
CONFRIMED = 1
UNCONFRIMED = 0
load_dotenv()
password = os.getenv("MYSQL_PASSWORD")

logger = setupLogger()

def getFriends(user_id,confirm = CONFRIMED):
    db = pymysql.connect(host="127.0.0.1",user="root",password=password,database=DATA_BASE)
    cursor = db.cursor()
    try:
        # 获取用户的好友列表
        db.begin()
        cursor.connection.ping(reconnect=True) 
        if confirm==CONFRIMED:
            sql = f"(SELECT friendId FROM {FRIEND_TABLE} WHERE userId = {user_id} and confirm = {CONFRIMED})\
            union (SELECT userId FROM {FRIEND_TABLE} WHERE friendId = {user_id} and confirm = {CONFRIMED});"
        else:
            sql = f"(SELECT userId FROM {FRIEND_TABLE} WHERE friendId = {user_id} and confirm = {UNCONFRIMED})"
        cursor.execute(sql)
        result = cursor.fetchall()
        friends = []
        for row in result:
            friends.append(row[0])   
    except Exception as e:
        logger.error(e,exc_info=True)
    finally:
        cursor.close()
        db.close()
    return friends if friends else None

def addFriend(user_id, friend_id):
    db = pymysql.connect(host="127.0.0.1",user="root",password=password,database=DATA_BASE)
    cursor = db.cursor()
    status = OTHER_ERROR
    try:
        # 首先检查是否已经是好友关系
        db.begin()
        cursor.connection.ping(reconnect=True) 
        sql = f"(SELECT * FROM {FRIEND_TABLE} WHERE userId = {user_id} AND friendId = {friend_id})\
        union (SELECT * FROM {FRIEND_TABLE} WHERE userId = {friend_id} AND friendId = {user_id});"
        cursor.execute(sql)
        result = cursor.fetchall()
        row = result[0] if result else None
        if row:
            # 已经confirm
            if row[2]==1:
                return "{}",ALLREADY_FRIEND
            # 申请过了
            elif row[0]==user_id:
                return "{}",ALLREADY_APPLIED
            # 对面申请了
            elif row[0]==friend_id:
                sql = f"UPDATE {FRIEND_TABLE} SET confirm = 1 WHERE userId = {friend_id} AND friendId = {user_id}"
                cursor.execute(sql)
                db.commit()
                return "{}",SUCCESS
        # 最后添加好友    
        sql = f"INSERT INTO {FRIEND_TABLE} (userId, friendId,confirm) VALUES ({user_id}, {friend_id},0)"
        cursor.execute(sql)
    except Exception as e:
        db.rollback()
        logger.error("add friend error: "+str(e))
        status = OTHER_ERROR
    else:
        db.commit()
        status = SUCCESS
    finally:
        cursor.close()
        db.close()
    return "{}",status
    
def confirmFriend(user_id, friend_id, confirm_message:int):
    db = pymysql.connect(host="127.0.0.1",user="root",password=password,database=DATA_BASE)
    cursor = db.cursor()
    status = OTHER_ERROR
    try:
        # 首先检查是否已经是好友关系，只确认对方申请的好友关系
        cursor.connection.ping(reconnect=True) 
        
        sql_try = f"SELECT * FROM {FRIEND_TABLE} WHERE userId = {friend_id} AND friendId = {user_id} AND confirm = 0"
        cursor.execute(sql_try)
        result = cursor.fetchone()
        if not result:
            raise Exception("No such friend request")
        # 然后同意好友关系
        if confirm_message:            
            sql = f"UPDATE {FRIEND_TABLE} SET confirm = 1 WHERE userId = {friend_id} AND friendId = {user_id}"
        else:
            sql = f"DELETE FROM {FRIEND_TABLE} WHERE userId = {friend_id} AND friendId = {user_id}"
        cursor.execute(sql)
    except Exception as e:
        logger.error(e)
        status = OTHER_ERROR
    else:
        db.commit()
        status = SUCCESS
    finally:
        cursor.close()
        db.close()
    return "{}",status

def deleteFriend(user_id, friend_id):
    db = pymysql.connect(host="127.0.0.1",user="root",password=password,database=DATA_BASE)
    cursor = db.cursor()
    status = OTHER_ERROR
    try:
        # 首先检查是否已经是好友关系
        cursor.connection.ping(reconnect=True) 
        friends = getFriends(friend_id)
        if friends==None or user_id not in friends:
            return "{}",NOT_FRIEND
        
        sql = f"DELETE FROM {FRIEND_TABLE} WHERE userId = {user_id} AND friendId = {friend_id}"
        sql2 = f"DELETE FROM {FRIEND_TABLE} WHERE userId = {friend_id} AND friendId = {user_id}"
        cursor.execute(sql)
        cursor.execute(sql2)
    except Exception as e:
        logger.error(e)
        status = OTHER_ERROR
    else:
        db.commit()
        status = SUCCESS
    finally:
        cursor.close()
        db.close()
    return "{}",status

def getFriendsInfo(user_id,confirm=CONFRIMED):
    db = pymysql.connect(host="127.0.0.1",user="root",password=password,database=DATA_BASE)
    cursor = db.cursor()
    result,status = {},OTHER_ERROR
    if confirm == None:
        confirm = CONFRIMED
    try:
        # 获取用户的好友列表
        # logger.debug(user_id)
        friends = getFriends(user_id,confirm)
        if not friends:
            return jsonify({'friends':[]}),SUCCESS
            return "{}",NO_FRIENDS
        friends_info = []
        for friend_id in friends:
            sql =f"(SELECT userName FROM {USER_TABLE} WHERE userId = {friend_id})"
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                username = result[0]
                friends_info.append({"userid":friend_id,"username":username})
        logger.debug(friends_info)
        result = {'friends':friends_info}
        status = SUCCESS
    except Exception as e:
        logger.error(e)
        status = OTHER_ERROR
    finally:
        cursor.close()
        db.close()
    return jsonify(result),status

