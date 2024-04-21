import flask
from flask_cors import CORS
from flask import request, jsonify
import os
from dotenv import load_dotenv
import pymysql
from user_manage.login import login

app = flask.Flask(__name__)

CORS(app, resources=r'/*')

@app.route('/login', methods=['POST'])
def login_api():
    username = request.form.get('uname')
    password = request.form.get('password')
    return login(username, password)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8888)
    print("Good bye!")