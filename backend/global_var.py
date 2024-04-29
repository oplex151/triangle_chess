from backend.game import RoomManager

# 全局变量
global rooms
global sessions
global sid2uid

rooms:list[RoomManager] = []
sessions:list[int] = []
sid2uid:dict[str, int] = {}