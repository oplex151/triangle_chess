import flask
import os
from dotenv import load_dotenv
import pymysql
from flask import jsonify

DATA_BASE = "TriangleChess"
USER_TABLE = "user"

load_dotenv()
password = os.getenv("MYSQL_PASSWORD")

db = pymysql.connect(host="127.0.0.1",user="root",password=password,database=DATA_BASE)
cursor = db.cursor()

def login(username, password):
    select_query = "SELECT * FROM {0} WHERE UserID = {1} AND Password = {2}".format(USER_TABLE,"'"+username+"'", "'"+password+"'")
    print(select_query)
    cursor.execute(select_query)
    result = cursor.fetchone()
    if result:
        return '{"code":0}'
    else:
        return '{"code":-1}'