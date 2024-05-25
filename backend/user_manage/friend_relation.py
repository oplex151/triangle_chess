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

load_dotenv()
password = os.getenv("MYSQL_PASSWORD")

db = pymysql.connect(host="127.0.0.1",user="root",password=password,database=DATA_BASE)
cursor = db.cursor()

logger = setupLogger()

def getFriends(user_id):
    try:
        # 获取用户的好友列表
        cursor.connection.ping(reconnect=True) 
        sql = (f"SELECT friendId FROM {FRIEND_TABLE} WHERE userId = {user_id} ")
        cursor.execute(sql)
        result = cursor.fetchall()
        friends = []
        for row in result:
            friends.append(row[0])
        return friends
    except Exception as e:
        logger.error(e,exc_info=True)
        return None

def addFriend(user_id, friend_id):
    try:
        # 首先检查是否已经是好友关系
        cursor.connection.ping(reconnect=True) 
        if user_id in getFriends(friend_id):
            return "{}",ALLREADY_FRIEND
        sql = f"INSERT INTO {FRIEND_TABLE} (userId, friendId) VALUES ({user_id}, {friend_id})"
        sql2 = f"INSERT INTO {FRIEND_TABLE} (userId, friendId) VALUES ({friend_id}, {user_id})"
        cursor.execute(sql)
        cursor.execute(sql2)
        db.commit()
        return "{}",SUCCESS
    except Exception as e:
        logger.error("add friend error: "+str(e))
        return "{}",OTHER_ERROR

def deleteFriend(user_id, friend_id):
    try:
        # 首先检查是否已经是好友关系
        cursor.connection.ping(reconnect=True) 
        if user_id not in getFriends(friend_id):
            return "{}",NOT_FRIEND
        sql = f"DELETE FROM {FRIEND_TABLE} WHERE userId = {user_id} AND friendId = {friend_id}"
        sql2 = f"DELETE FROM {FRIEND_TABLE} WHERE userId = {friend_id} AND friendId = {user_id}"
        cursor.execute(sql)
        cursor.execute(sql2)
        db.commit()
        return "{}",SUCCESS
    except Exception as e:
        logger.error(e)
        return "{}",OTHER_ERROR

def getFriendsInfo(user_id):
    try:
        # 获取用户的好友列表
        logger.debug(user_id)
        friends = getFriends(user_id)
        if not friends:
            return "{}",NO_FRIENDS
        friends_info = []
        for friend_id in friends:
            sql =(f"SELECT username FROM {USER_TABLE} WHERE userId = {friend_id}") # sql可以优化
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                username = result[0]
                friends_info.append({"userid":friend_id,"username":username})
        logger.debug(friends_info)
        return jsonify({'friends':friends_info}),SUCCESS
    except Exception as e:
        logger.error(e)
        return "{}",OTHER_ERROR