import queue
from backend.game import RoomManager

# 全局变量
global rooms
global sessions
global sid2uid
global match_queue

rooms:list[RoomManager] = []
sessions:dict[int, str] = {}
match_queue:queue.Queue = queue.Queue()
sid2uid:dict[str, int] = {}


def uid2sid(uid:int)->str:
    for sid, u in sid2uid.items():
        if u == uid:
            return sid
    return None

