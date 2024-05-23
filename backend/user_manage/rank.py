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

def viewUserRank(userid:int):
    try:
        select_query = "SELECT rank, score FROM {0} WHERE userId = {1};".format(USER_TABLE, userid)
        cursor.execute(select_query)
        result = cursor.fetchone()
        if result is None:
            logger.error("User {0} not exists".format(userid))
            return None
        return result
    except Exception as e:
        logger.error("User {0} failed to view rank due to\n{1}".format(userid,str(e)))
        return None