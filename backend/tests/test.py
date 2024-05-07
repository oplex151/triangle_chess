import sys
import os
import json
from pathlib import Path
  

#设置环境变量PROJECT_ROOT
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
os.environ['PROJECT_ROOT'] = str(Path(__file__).resolve().parent.parent.parent)
print(os.environ['PROJECT_ROOT'])

from backend.tools import setupLogger 
from backend.game import GameTable

logger = setupLogger()

def test1():
    game = GameTable([11, 12, 13])
    print(game.movePiece(11,0,0,0,0,0,1))
    print(game.movePiece(12,0,0,1,0,0,1))
    print(game.movePiece(11,2,0,2,0,0,1))
    
    game.showBoard()
    # print(game.getGameInfo())
    # with open('./backend/tests/test.json', 'w') as f:
    #     json.dump(game.getGameInfo(), f, indent=4)

def test2():
    pass

if __name__ == '__main__':
    test1()
    print('测试完成')