from functools import wraps
import os
import pymysql
import base64
from io import BytesIO
from PIL import Image
import datetime
import jwt #装PyJWT
import hashlib
from dotenv import load_dotenv
from flask import jsonify
from backend.tools import setupLogger
from backend.message import *
from backend.global_var import rooms,sessions

DATA_BASE = "trianglechess" # 数据库名称
USER_TABLE = "user"

load_dotenv()
db_password = os.getenv("MYSQL_PASSWORD")

logger = setupLogger()

def base64ToImage(base64_str:str):  # 用 b.show()可以展示
    try:
        sstr = base64_str.find("base64,")
        if sstr == -1:
            raise ValueError("Invalid base64 string")
        header = base64_str[:sstr+7]
        ext = header.split("/")[-1].split(";")[0]
        if ext  == 'svg+xml':
            image = base64.b64decode(base64_str[sstr+7:])
            return image,"svg"
        else:
            base64_str = base64_str[sstr+7:]
            # print(base64_str)
            image = base64.b64decode(base64_str, altchars=None, validate=False)
        image = Image.open(BytesIO(image))
        return image,ext
    except Exception as e:
        print(e)
        raise ValueError("Invalid base64 string")

def saveImage(image,path,ext):
    if ext == "svg":
        with open(path,"wb") as f:
            f.write(image)
    else:
        image.save(path)

def hash_token(password):
    # 使用SHA-256算法加密密码
    return hashlib.sha256(password.encode()).hexdigest()

def validate_token(plain_password, hashed_password):
    return hash_token(plain_password) == hashed_password

def adminLogin(password, config_password):
    #if not protected_route(request.headers.get('Authorization').split(' ')[1]):
    res = {} 
    if password == 'sanguoxiangqi':
        token = jwt.encode({'role':'admin','exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, config_password)
        res['token'] = token
        return jsonify(res),SUCCESS
    else:
        return jsonify(res),OTHER_ERROR


def login(username, password):
    global sessions
    db = pymysql.connect(host="127.0.0.1",user="root",password=db_password,database=DATA_BASE)
    cursor = db.cursor()
    res,status = {},None
    try:
        db.begin()
        select_query = "SELECT userPassword, userId, banned FROM {0} WHERE userName = {1};".format(USER_TABLE,"'"+username+"'")
        cursor.execute(select_query)
        result = cursor.fetchone()
        if result is not None and result[0] == password:
            if result[2] == 1:
                logger.error("User {0} is banned".format(username))
                return "{}",BANNED_USER
            if result[1] in sessions:
                logger.error("User {0} already logged in".format(username))
                return "{}",ALREADY_LOGIN
            logger.info("User {0} logged in successfully usring id {1}".format(username,result[1]))
            res = {"userid":result[1], "username":username}
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
    

def register(username, password, email, phone_num, gender):
    db = pymysql.connect(host="127.0.0.1",user="root",password=db_password,database=DATA_BASE)
    cursor = db.cursor()
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


def changeUserInfo(userid:int, username:str=None, email:str=None, phone_num:str=None, gender:str=None):
    db = pymysql.connect(host="127.0.0.1",user="root",password=db_password,database=DATA_BASE)
    cursor = db.cursor()
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


def changePassword(userid:int, old_password:str, new_password:str):
    db = pymysql.connect(host="127.0.0.1",user="root",password=db_password,database=DATA_BASE)
    cursor = db.cursor()
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


def getUserInfo(userid:int):
    db = pymysql.connect(host="127.0.0.1",user="root",password=db_password,database=DATA_BASE)
    cursor = db.cursor()
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
        dic["userid"] = data[0]
        dic["username"] = data[1]
        dic['rank'] = data[3]
        dic['score'] = data[4]
        dic['gender'] = data[5]
        dic['phone_num'] = data[6]
        dic['email'] = data[7]
        dic['image_path'] = data[8]
        status = SUCCESS
    except Exception as e:
        logger.error("User {0} failed to get user info due to\n{1}".format(userid,str(e)),exc_info=True)
        status = OTHER_ERROR
    finally:
        cursor.close()
        db.close()
    return jsonify(dic),status


def getSomeUserAvatar(userids:list[int]):
    db = pymysql.connect(host="127.0.0.1",user="root",password=db_password,database=DATA_BASE)
    cursor = db.cursor()
    dic, status = {}, None
    try:
        # 首先就检查用户名是否已经存在
        db.begin()
        for userid in userids:
            
            select_query = "SELECT * FROM {0} WHERE userId = {1};".format(USER_TABLE, userid)
            cursor.execute(select_query)
            data = cursor.fetchone()
            if data is None:
                logger.error("User {0} not exists".format(userid))
                dic[userid] = None
            else:
                dic[userid] = data[8]
            status = SUCCESS
    except Exception as e:
        logger.error("User {0} failed to get user info due to\n{1}".format(userid,str(e)),exc_info=True)
        status = OTHER_ERROR
    finally:
        cursor.close()
        db.close()
    # 没有jsonify
    return dic,status


def uploadImage(userid:int, image:str):
    db = pymysql.connect(host="127.0.0.1",user="root",password=db_password,database=DATA_BASE)
    cursor = db.cursor()
    res,status = {},None
    # 后台接收到base64，把base64转成图片，存到文件服务器里面，根据存储的路径生成图片的url
    # 存到数据库里面，记录图片的路径
    # 前端根据图片路径显示图片
    try:    
        img,ext = base64ToImage(image)
        image_path = '/static/'+str(userid)+ "."+ext
        saveImage(img,os.environ.get('PROJECT_ROOT')+'/backend'+image_path,ext)
        db.begin()
        update_query = "UPDATE {0} SET imagePath = {1} WHERE userId = {2};".format(USER_TABLE,"'"+image_path+"'",userid)
        cursor.execute(update_query)
        db.commit()
        res = {"image_path":image_path}
        logger.info("User {0} uploaded image successfully".format(userid))
    except Exception as e:
        logger.error("Use0} failed to upload image due to\n{1}".format(userid,str(e)),exc_info=True)
        status = OTHER_ERROR if status is None else status
    finally:
        cursor.close()
        db.close()
    return jsonify(res),status


def getUserData():
    db = pymysql.connect(host="127.0.0.1",user="root",password=db_password,database=DATA_BASE)
    cursor = db.cursor()
    res,status = [],None
    try:
        db.begin()
        select_query = "SELECT * FROM {0};".format(USER_TABLE)
        cursor.execute(select_query)
        data = cursor.fetchall()
        for i in data:
            dic = {}
            dic["userid"] = i[0]
            dic["username"] = i[1]
            dic['rank'] = i[3]
            dic['score'] = i[4]
            dic['gender'] = i[5]
            dic['phone_num'] = i[6]
            dic['email'] = i[7]
            dic['image_path'] = i[8]
            dic['banned'] = i[9]
            res.append(dic)
        status = SUCCESS
    except Exception as e:
        logger.error("Failed to get user data due to\n{0}".format(str(e)),exc_info=True)
        status = OTHER_ERROR
    finally:
        cursor.close()
        db.close()
    return jsonify(res),status

def changeUserBanned(userid:int, banned:int):
    db = pymysql.connect(host="127.0.0.1",user="root",password=db_password,database=DATA_BASE)
    cursor = db.cursor()
    res,status = {},None
    try:
        db.begin()
        select_query = "SELECT * FROM {0} WHERE userId = {1};".format(USER_TABLE, userid)
        cursor.execute(select_query)
        data = cursor.fetchone()
        if data is None:
            logger.error("User {0} not exists".format(userid))
            return None,USER_NOT_EXIST
        if data[9] == 1 and banned == 1:
            logger.error("User {0} is already banned".format(userid))
            return None,USER_ALREADY_BANNED
        update_query = "UPDATE {0} SET banned = {1} WHERE userId = {2};".format(USER_TABLE,banned, userid)
        cursor.execute(update_query)
        db.commit()
        logger.info("User {0} banned successfully".format(userid))
        status = SUCCESS
    except Exception as e:
        logger.error("User {0} failed to ban due to\n{1}".format(userid,str(e)),exc_info=True)
        status = OTHER_ERROR
    finally:
        cursor.close()
        db.close()
    return jsonify(res),status