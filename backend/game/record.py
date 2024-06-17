import os
import pymysql
import datetime
from dotenv import load_dotenv

from backend.tools import setupLogger
from backend.message import *

'''
this is a module for handling game records in the database.

The database has two tables: game_record and game_move.

game_record table:
- recordId: unique id for each game record
- p1: player 1's id
- p2: player 2's id
- p3: player 3's id
- startTime: start time of the game
- endTime: end time of the game
- winner: winner's id
- likeNum: number of likes for this game
- commentNum: number of comments for this game


game_move table:
- recordId: foreign key to game_record table
- playerId: player who made the move
- chessType: type of chess piece moved
- startPos: start position of the chess piece
- endPos: end position of the chess piece

The module provides functions for inserting new game records, recording moves, and ending games.

but it will save all the game records in the database, no matter if the users want to keep them or not.
'''


DATA_BASE = "trianglechess"
GAME_RECORD_TABLE = "game_record"
GAME_MOVE_TABLE = "game_move"
COMMENT_TABLE = "comment"

load_dotenv()
password = os.getenv("MYSQL_PASSWORD")


logger = setupLogger()

def initRecord(p1, p2, p3, start_time=None, end_time=None, winner=None, like_num=0, comment_num=0):
    record_id = None
    status = OTHER_ERROR
    try:
        db = pymysql.connect(host="127.0.0.1",user="root",password=password,database=DATA_BASE,cursorclass=pymysql.cursors.DictCursor)
        cursor = db.cursor()
        db.begin()
        insert_query = """
            INSERT INTO {0} (p1, p2, p3, startTime, endTime, winner, likeNum, commentNum)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """.format(GAME_RECORD_TABLE)
        start_time = datetime.datetime.now()
        end_time=datetime.datetime.now()
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
        record_id = cursor.fetchone()['LAST_INSERT_ID()']
    except Exception as e:
        db.rollback()
        logger.error("Failed to insert new record due to\n{0}".format(str(e)),exc_info=True)
        record_id = None
    finally:
        cursor.close()
        db.close()
    return record_id

class GameRecord:
    def __init__(self, p1, p2, p3, start_time=None, end_time=None, winner=None, like_num=0, comment_num=0):
        self.record_id = initRecord(p1, p2, p3)
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.start_time = datetime.datetime.now()
        self.end_time = end_time
        self.winner = winner
        self.like_num = like_num
        self.comment_num = comment_num

    def recordMove(self, playerId, chessType, startPos, endPos):
        status = OTHER_ERROR
        try:
            db = pymysql.connect(host="127.0.0.1",user="root",password=password,database=DATA_BASE,cursorclass=pymysql.cursors.DictCursor)
            cursor = db.cursor()
            db.begin()
            insert_query = "INSERT INTO {0} (recordId, playerId, chessType, startPos, endPos) VALUES (%s, %s, %s, %s, %s);".format(GAME_MOVE_TABLE)
            cursor.execute(insert_query, (self.record_id, playerId, chessType, startPos, endPos))
            db.commit()
            logger.info("Recorded move for game {0} successfully".format(self.record_id))
            status = SUCCESS
        except Exception as e:
            db.rollback()
            logger.error("Failed to record move for game {0} due to\n{1}".format(self.record_id, str(e)))
            status = OTHER_ERROR
        finally:
            cursor.close()
            db.close()
        return status
        
    def recordEnd(self, winnerid):
        # self.end_time = datetime.datetime.now(),  # 对局结束时间为当前时间
        self.winner = winnerid
        status = OTHER_ERROR
        try:
            db = pymysql.connect(host="127.0.0.1",user="root",password=password,database=DATA_BASE,cursorclass=pymysql.cursors.DictCursor)
            cursor = db.cursor()
            db.begin()
            # 更新数据库中的对局记录
            update_query = "UPDATE {0} SET endTime = %s, winner = %s WHERE recordId = %s;".format(GAME_RECORD_TABLE)
            cursor.execute(update_query, (self.end_time, self.winner, self.record_id))
            db.commit()
            
            logger.info("Record {0} ended. Winner: {1}".format(self.record_id, winnerid))
            status = SUCCESS
        except Exception as e:
            db.rollback()
            logger.error("Failed to end record {0} due to\n{1}".format(self.record_id, str(e)))
            status = OTHER_ERROR
        finally:
            cursor.close()
            db.close()
        return status,self.record_id

def viewUserGameRecords(user_id):
    status = OTHER_ERROR
    records = None
    try:
        db = pymysql.connect(host="127.0.0.1",user="root",password=password,database=DATA_BASE,cursorclass=pymysql.cursors.DictCursor)
        cursor = db.cursor()
        db.begin()
        # 查询特定用户参与的游戏记录
        select_query = "SELECT DISTINCT * FROM {0} WHERE p1=%s OR p2=%s OR p3=%s ORDER BY startTime DESC;".format(GAME_RECORD_TABLE)
        cursor.execute(select_query, (user_id, user_id, user_id))
        records = cursor.fetchall()
        for record in records:
            # 查询每个记录的走棋记录
            record['startTime'] = record['startTime'].strftime("%Y-%m-%dT%H:%M:%S")
            record['endTime'] = record['endTime'].strftime("%Y-%m-%dT%H:%M:%S") if record['endTime'] else None
        status = SUCCESS
    except Exception as e:
        # db.rollback()
        logger.error("Failed to view user {0} game records: due to\n{1}".format(user_id, str(e)))
        status = OTHER_ERROR
    finally:
        cursor.close()
        db.close()
    return records,status

def viewAllVisibleGameRecords():
    status = OTHER_ERROR
    records = None
    try:
        db = pymysql.connect(host="127.0.0.1",user="root",password=password,database=DATA_BASE,cursorclass=pymysql.cursors.DictCursor)
        cursor = db.cursor()
        db.begin()
        # 查询所有可见的游戏记录
        select_query = "SELECT * FROM {0} WHERE visible=1 ORDER BY startTime DESC;".format(GAME_RECORD_TABLE)
        cursor.execute(select_query)
        records = cursor.fetchall()
        for record in records:
            # 查询每个记录的走棋记录
            record['startTime'] = record['startTime'].strftime("%Y-%m-%dT%H:%M:%S")
            record['endTime'] = record['endTime'].strftime("%Y-%m-%dT%H:%M:%S") if record['endTime'] else None
        status = SUCCESS
    except Exception as e:
        # db.rollback()
        logger.error("Failed to view all visible game records: due to\n{0}".format(str(e)))
        status = OTHER_ERROR
    finally:
        cursor.close()
        db.close()
    
    return records,status

def changeGameRecordVisible(record_id, visible):
    status = OTHER_ERROR
    try:
        # 更新游戏记录的可见性
        db = pymysql.connect(host="127.0.0.1",user="root",password=password,database=DATA_BASE)
        cursor = db.cursor()
        db.begin()
        #print(visible,record_id)
        update_query = "UPDATE {0} SET visible={1} WHERE recordId={2};".format(GAME_RECORD_TABLE,visible, record_id)
        cursor.execute(update_query)
        db.commit()
        logger.info("Changed game record {0} visible to {1}".format(record_id, visible))
        status = SUCCESS
    except Exception as e:
        db.rollback()
        logger.error("Failed to change game record {0} visible to {1} due to\n{2}".format(record_id, visible, str(e)))
        status = OTHER_ERROR
    finally:
        cursor.close()
        db.close()
    return '{}',status



def viewGameMoveRecords(record_id):
    status = OTHER_ERROR
    records = None
    try:
        db = pymysql.connect(host="127.0.0.1",user="root",password=password,database=DATA_BASE,cursorclass=pymysql.cursors.DictCursor)
        cursor = db.cursor()
        db.begin()
        # 查询特定用户参与的游戏记录
        select_query = "SELECT DISTINCT * FROM {0} WHERE recordId = %s ORDER BY moveId ASC;".format(GAME_MOVE_TABLE)
        cursor.execute(select_query, (record_id))
        records = cursor.fetchall()
        for record in records:
            # 查询每个记录的走棋记录
            record['timestamp'] = record['timestamp'].strftime("%Y-%m-%dT%H:%M:%S")
        status = SUCCESS
    except Exception as e:
        # db.rollback()
        logger.error("Failed to view game records {0} moves: due to\n{1}".format(record_id, str(e)))
        status = OTHER_ERROR
    finally:
        cursor.close()
        db.close()
    return records,status
    
def likeGameRecord(record_id):
    # 点赞功能
    status = OTHER_ERROR
    try:
        db = pymysql.connect(host="127.0.0.1",user="root",password=password,database=DATA_BASE,cursorclass=pymysql.cursors.DictCursor)
        cursor = db.cursor()
        db.begin()
        update_query = "UPDATE {0} SET likeNum = likeNum + 1 WHERE recordId = %s;".format(GAME_RECORD_TABLE)
        cursor.execute(update_query, (record_id))
        db.commit()
        logger.info("Record {0} liked successfully".format(record_id))
        status = SUCCESS
    except Exception as e:
        db.rollback()
        logger.error("Failed to like record {0} due to\n{1}".format(record_id, str(e)))
        status = OTHER_ERROR
    finally:
        cursor.close()
        db.close()
    return "{}",status

def unlikeGameRecord(record_id):
    status = OTHER_ERROR
    # 取消点赞功能
    try:
        db = pymysql.connect(host="127.0.0.1",user="root",password=password,database=DATA_BASE,cursorclass=pymysql.cursors.DictCursor)
        cursor = db.cursor()
        db.begin()
        update_query = "UPDATE {0} SET likeNum = likeNum - 1 WHERE recordId = %s AND likeNum > 0;".format(GAME_RECORD_TABLE)
        cursor.execute(update_query, (record_id))
        db.commit()
        logger.info("Record {0} unliked successfully".format(record_id))
        status = SUCCESS
    except Exception as e:
        db.rollback()
        logger.error("Failed to unlike record {0} due to\n{1}".format(record_id, str(e)))
        status = OTHER_ERROR
    finally:
        cursor.close()
        db.close()
    return "{}",status

def addComment(record_id, user_id, content):
    # 添加评论功能
    status = OTHER_ERROR
    try:
        db = pymysql.connect(host="127.0.0.1",user="root",password=password,database=DATA_BASE,cursorclass=pymysql.cursors.DictCursor)
        cursor = db.cursor()
        insert_query = "INSERT INTO {0} (recordId, userId, content, commentTime) VALUES (%s, %s, %s, %s);".format(COMMENT_TABLE)
        comment_time = datetime.datetime.now()
        cursor.execute(insert_query, (record_id, user_id, content, comment_time))
        db.commit()

        update_query = "UPDATE {0} SET commentNum = commentNum + 1 WHERE recordId = %s;".format(GAME_RECORD_TABLE)
        cursor.execute(update_query, (record_id))
        db.commit()

        logger.info("Comment added to record {0} by user {1}".format(record_id, user_id))
        status = SUCCESS
    except Exception as e:
        db.rollback()
        logger.error("Failed to add comment to record {0} by user {1} due to\n{2}".format(record_id, user_id, str(e)))
        status = OTHER_ERROR
    finally:
        cursor.close()
        db.close()
    return "{}",status

def likeComment(comment_id):
    status = OTHER_ERROR
    # 点赞评论功能
    try:
        db = pymysql.connect(host="127.0.0.1",user="root",password=password,database=DATA_BASE,cursorclass=pymysql.cursors.DictCursor)
        cursor = db.cursor()
        db.begin()
        update_query = "UPDATE {0} SET likeNum = likeNum + 1 WHERE commentId = %s;".format(COMMENT_TABLE)
        cursor.execute(update_query, (comment_id))
        db.commit()
        logger.info("Comment {0} liked successfully".format(comment_id))
        status = SUCCESS
    except Exception as e:
        db.rollback()
        logger.error("Failed to like comment {0} due to\n{1}".format(comment_id, str(e)))
        status = OTHER_ERROR
    finally:
        cursor.close()
        db.close()
    return "{}",status

def unlikeComment(comment_id):
    status = OTHER_ERROR
    # 取消点赞评论功能
    try:
        db = pymysql.connect(host="127.0.0.1",user="root",password=password,database=DATA_BASE,cursorclass=pymysql.cursors.DictCursor)
        cursor = db.cursor()
        db.begin()
        update_query = "UPDATE {0} SET likeNum = likeNum - 1 WHERE commentId = %s AND likeNum > 0;".format(COMMENT_TABLE)
        cursor.execute(update_query, (comment_id))
        db.commit()
        logger.info("Comment {0} unliked successfully".format(comment_id))
        status = SUCCESS
    except Exception as e:
        db.rollback()
        logger.error("Failed to unlike comment {0} due to\n{1}".format(comment_id, str(e)))
        status = OTHER_ERROR
    finally:
        cursor.close()  
        db.close()
    return "{}",status
    
def viewRecordComments(record_id):
    status = OTHER_ERROR
    try:
        db = pymysql.connect(host="127.0.0.1",user="root",password=password,database=DATA_BASE,cursorclass=pymysql.cursors.DictCursor)
        cursor = db.cursor()
        db.begin()
        # 查询特定对局记录的所有评论
        select_query = "SELECT * FROM {0} WHERE recordId = %s ORDER BY commentTime ASC;".format(COMMENT_TABLE)
        cursor.execute(select_query, (record_id,))
        comments = cursor.fetchall()
        for comment in comments:
            comment['commentTime'] = comment['commentTime'].strftime("%Y-%m-%dT%H:%M:%S")
        status = SUCCESS
    except Exception as e:
        logger.error("Failed to view comments for record {0} due to\n{1}".format(record_id, str(e)))
        status = OTHER_ERROR
    finally:
        cursor.close()
        db.close()
    return comments,status