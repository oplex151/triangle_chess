import queue
from backend.game import RoomManager

# 全局变量
global rooms
global sessions
global sid2uid

rooms:list[RoomManager] = []
sessions:list[int] = []
match_queue:queue = queue.Queue()
sid2uid:dict[str, int] = {}