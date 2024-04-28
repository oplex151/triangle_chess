import sys
import os
from pathlib import Path

#设置环境变量PROJECT_ROOT
sys.path.append(str(Path(__file__).resolve().parent.parent))
os.environ['PROJECT_ROOT'] = str(Path(__file__).resolve().parent.parent)

from game import GameTable

def test1():
    game = GameTable('user1', 'user2', 'user3')
    game.movePiece('user1',0,0,0,1,0,0)


if __name__ == '__main__':
    test1()
    print('测试完成')