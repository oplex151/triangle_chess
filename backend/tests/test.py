import sys
import os
import json
from pathlib import Path
  

#设置环境变量PROJECT_ROOT
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
os.environ['PROJECT_ROOT'] = str(Path(__file__).resolve().parent.parent.parent)
print(os.environ['PROJECT_ROOT'])

from backend.tools import setupLogger 
from backend.game import GameTable,UserDict

logger = setupLogger()


def test1():
    user_list = [UserDict(userid=11, username='user1'), UserDict(userid=-12, username='user2'), UserDict(userid=13, username='user3')]
    game = GameTable(user_list)
    print(game.movePiece(11,0,0,0,0,0,1))
    print(game.movePiece(12,0,0,1,0,0,1))
    print(game.movePiece(11,2,0,2,0,0,1))
    game.showBoard()

def test2():
    user_list = [UserDict(userid=11, username='user1'), UserDict(userid=-12, username='user2'), UserDict(userid=13, username='user3')]
    game = GameTable(user_list)
    print(game.movePiece(11,0,3,0,0,4,0))
    print(game.movePiece(12,0,3,1,0,4,1))
    game.showBoard()
    

def test3():
    user_list = [UserDict(userid=11, username='user1'), UserDict(userid=-12, username='user2'), UserDict(userid=13, username='user3')]
    game = GameTable(user_list)
    with open(os.environ['PROJECT_ROOT']+'/backend/tests/test.json', 'w') as f:
        json.dump(game.getGameInfo(), f, indent=4)

if __name__ == '__main__':
    #test1()
    #test2()
    test3()
    print('测试完成')