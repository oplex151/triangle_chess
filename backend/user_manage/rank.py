from functools import wraps
import os
import pymysql
from dotenv import load_dotenv
from flask import jsonify
from backend.tools import setupLogger
from backend.message import *
from backend.global_var import rooms,sessions
from backend.game import *

DATA_BASE = "trianglechess" # 数据库名称
USER_TABLE = "user"

load_dotenv()
password = os.getenv("MYSQL_PASSWORD")

db = pymysql.connect(host="127.0.0.1",user="root",password=password,database=DATA_BASE)
cursor = db.cursor()

def connectDatabase(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        global db, cursor
        db = pymysql.connect(host="127.0.0.1",user="root",password=password,database=DATA_BASE)
        cursor = db.cursor()
        return func(*args, **kwargs)
    return wrapper

logger = setupLogger()

#100积分晋升一个段位
#初步设定，假设每个段位相同积分晋升
rankscore = 100

@connectDatabase
def viewUserRank(userid:int):
    result = None
    try:
        db.begin()
        select_query = "SELECT rank, score FROM {0} WHERE userId = {1};".format(USER_TABLE, userid)
        cursor.execute(select_query)
        result = cursor.fetchone()
        if result is None:
            logger.error("User {0} not exists".format(userid))
    except Exception as e:
        logger.error("User {0} failed to view rank due to\n{1}".format(userid,str(e)))
        result = None
    finally:
        cursor.close()
        db.close()
    return result

def totalScore(rank, score):
    """
    根据段位和积分计算玩家的总积分。
    Args:
        rank: 玩家的段位
        score: 玩家的积分
    
    Returns:
        totalscore: 总积分
    """
    totalscore = rank * rankscore + score
    return totalscore 

def rankScore(totalscore):
    """
    根据总积分计算玩家的段位和积分。
    Args:
        totalscore: 总积分
    
    Returns:
        rank: 玩家的段位
        score: 玩家的积分
    """
    rank = totalscore / rankscore
    score = totalscore % rankscore
    return rank, score 

def isEligible(user1, user2):
    rank_diff = abs(user1[1] - user2[1])
    totalscore_diff = abs(totalScore(user1[1],user1[2]) - totalScore(user2[1],user2[2]))
    return rank_diff <= 1 and totalscore_diff <= 150  # 假设允许的段位差和最大总积分差

def calculatePerformance(captured_pieces, opponent_captured_pieces):
    """
    根据游戏中的表现评定各个玩家的表现评分。
    
    Args:
        captured_pieces: 各个玩家捕获的对手棋子
        opponent_captured_pieces: 各个对手捕获的玩家棋子
    
    Returns:
        performance: 表现评分
    """
    piece_score = {
        "Soilder": 1,   # 兵的得分
        "Gun": 3,       # 炮的得分
        "Chariot": 5,   # 车的得分
        "WarHorse": 4,  # 马的得分
        "Bishop": 2,    # 象的得分
        "Advisor": 2,   # 士的得分
        "Leader": 10    # 将的得分
    }
    
    # 计算玩家和对手的总得分
    player_score = sum([piece_score[piece.name] for piece in captured_pieces])
    opponent_score = sum([piece_score[piece.name] for piece in opponent_captured_pieces])
    
    # 最终得分为玩家得分减去对手得分
    performance = player_score - opponent_score
    
    return performance

def calculateNewScore(player_score, opponent_scores, result, player_performance):
    """
    计算新排位积分。
    
    Args:
        player_score: 玩家当前的总积分
        opponent_scores: 对手的总积分列表
        result: 比赛结果，"win","lose"或"draw"
        performance: 玩家表现评分
    
    Returns:
        new_score: 新的排位积分
    """
    rank, score = rankScore(player_score)
    base_win_score = 25 - rank
    base_draw_score = 5 - rank
    base_lose_score = -15 - rank
    performance_factor = 0.1
    opponent_factor = 0.05
    
    average_opponent_score = sum(opponent_scores) / len(opponent_scores)
    opponent_diff = average_opponent_score - player_score

    if result == "win":
        new_score = player_score + base_win_score + (performance_factor * player_performance) + (opponent_factor * opponent_diff)
    elif result == "lose":
        new_score = player_score + base_lose_score + (performance_factor * player_performance) + (opponent_factor * opponent_diff)
    elif result == "draw":
        new_score = player_score + base_draw_score + (performance_factor * player_performance) + (opponent_factor * opponent_diff)
    else:
        raise ValueError("Invalid result: should be 'win' or 'lose' or 'draw'")
    
    return round(new_score)

@connectDatabase
def updateUserRank(userid, rank, score):
    # 实现将新段位积分更新到数据库中
    result = False
    try:
        db.begin()
        update_query = "UPDATE {0} SET rank = {1}, score = {2} WHERE userid = {3}".format(USER_TABLE, rank, score, userid)
        cursor.execute(update_query)
        result = True
    except Exception as e:
        db.rollback()
        print("User {0} Error updating rank due to\n{1}".format(userid,str(e)))
        result = False
    else:
        db.commit()
    finally:
        cursor.close()
        db.close()
    return result

def endRankGame(game:GameTable):
    """
    结束排位游戏时更新所有玩家的排位积分。
    
    Args:
        game: 当前对局的 GameTable 对象，包含玩家信息和比赛结果
    """
    for user in game.users:
        userid = user['userid']
        user_z = game._getUserIndex(userid)
        rank, score = viewUserRank(userid)  # 从数据库获取玩家当前积分
        player_score = totalScore(rank, score)
        opponent_rs = [viewUserRank(opponent['userid']) for opponent in game.users if opponent['userid'] != userid]
        opponent_scores = [totalScore(orank, oscore) for orank, oscore in opponent_rs]
        result = game.getUserResult(userid)  # 获取玩家的比赛结果
        player_performance = calculatePerformance(game.captured_pieces[user_z], game.opponent_captured_pieces[user_z]) # 获取玩家的表现评分

        new_score = calculateNewScore(player_score, opponent_scores, result, player_performance)
        updateUserRank(userid, new_score)  # 将新积分更新到数据库中