import os
import pymysql
import datetime
from dotenv import load_dotenv

from backend.tools import setupLogger
from backend.message import *


DATA_BASE = "trianglechess"
GAME_RECORD_TABLE = "game_record"
GAME_MOVE_TABLE = "game_move"

load_dotenv()
password = os.getenv("MYSQL_PASSWORD")

db = pymysql.connect(host="127.0.0.1",user="root",password=password,database=DATA_BASE)
cursor = db.cursor()

logger = setupLogger()

def initRecord(p1, p2, p3, start_time=datetime.datetime.now(), end_time=None, winner=None, like_num=0, comment_num=0):
    try:
        insert_query = """
            INSERT INTO {0} (p1, p2, p3, startTime, endTime, winner, likeNum, commentNum)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """.format(GAME_RECORD_TABLE)
        cursor.execute(insert_query, (
            p1,
            p2,
            p3,
            start_time,
            end_time,
            winner,
            like_num,
            comment_num
        ))
        db.commit()
        logger.info("Inserted new record successfully")
        # 获取刚插入的记录的 recordId
        select_query = "SELECT LAST_INSERT_ID()"
        cursor.execute(select_query)
        record_id = cursor.fetchone()[0]
        return record_id
    except Exception as e:
        db.rollback()
        logger.error("Failed to insert new record due to\n{0}".format(str(e)))
        return None

class GameRecord:
    def __init__(self, p1, p2, p3, start_time=datetime.datetime.now(), end_time=None, winner=None, like_num=0, comment_num=0):
        self.record_id = initRecord(p1, p2, p3)
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.start_time = start_time
        self.end_time = end_time
        self.winner = winner
        self.like_num = like_num
        self.comment_num = comment_num

    def recordMove(self, playerId, chessType, startPos, endPos):
        try:
            insert_query = "INSERT INTO {0} (recordId, playerId, chessType, startPos, endPos) VALUES (%s, %s, %s, %s, %s, %s);".format(GAME_MOVE_TABLE)
            cursor.execute(insert_query, (self.record_id, playerId, chessType, startPos, endPos))
            db.commit()
            logger.info("Recorded move for game {0} successfully".format(self.record_id))
            return SUCCESS
        except Exception as e:
            db.rollback()
            logger.error("Failed to record move for game {0} due to\n{1}".format(self.record_id, str(e)))
            return OTHER_ERROR
        
    def recordEnd(self, winnerid):
        self.end_time = datetime.datetime.now(),  # 对局结束时间为当前时间
        self.winner = winnerid
        try:
            # 更新数据库中的对局记录
            update_query = "UPDATE {0} SET endTime = %s, winner = %s WHERE recordId = %s;".format(GAME_RECORD_TABLE)
            cursor.execute(update_query, (self.end_time, self.winner, self.record_id))
            db.commit()
            
            logger.info("Record {0} ended. Winner: {1}".format(self.record_id, winnerid))
            return SUCCESS
        except Exception as e:
            db.rollback()
            logger.error("Failed to end record {0} due to\n{1}".format(self.record_id, str(e)))
            return OTHER_ERROR

def viewUserGameRecords(user_id):
    try:
        # 查询特定用户参与的游戏记录
        select_query = "SELECT * FROM {0} WHERE p1=%s OR p2=%s OR p3=%s ORDER BY startTime DESC;".format(GAME_RECORD_TABLE)
        cursor.execute(select_query, (user_id, user_id, user_id))
        records = cursor.fetchall()
        return records,SUCCESS
    except Exception as e:
        db.rollback()
        logger.error("Failed to view user {0} game records: due to\n{1}".format(user_id, str(e)))
        return None,OTHER_ERROR