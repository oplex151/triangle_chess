import queue
from backend.game import RoomManager

# 全局变量
global rooms
global sessions
global session_times
global sid2uid
global match_queue
global rank_queue

def uid2sid(uid:int)->str:
    global sid2uid
    for sid, u in sid2uid.items():
        if u == uid:
            return sid
    return None

class UniqueQueue(queue.Queue):
    def _init(self, maxsize):
        self.queue_set = set()
        super()._init(maxsize)

    def put(self, item):
        if item not in self.queue_set:
            self.queue_set.add(item)
            super()._put(item)

    def get(self):
        if not self.queue_set.__len__():
            raise queue.Empty
        item = super()._get()
        while item not in self.queue_set:
            item = super()._get()
            continue
        self.queue_set.remove(item)
        return item
    
    def is_have(self, item):
        return item in self.queue_set
    
    def remove(self, item):
        if item in self.queue_set:
            self.queue_set.remove(item)
        
    def qsize(self) -> int:
        return self.queue_set.__len__()
  

rooms:list[RoomManager] = []
sessions:dict[int, str] = {}
session_times:dict[int, float] = {}
match_queue:UniqueQueue = UniqueQueue()
sid2uid:dict[str, int] = {}
rank_queue:UniqueQueue = UniqueQueue()

if __name__ == '__main__':
    q = UniqueQueue()
    q.put(1)
    q.put(2)
    q.put(3)
    q.put(2)
    q.put(4)
    print(q.get())
    print(q.get())
    print(q.get())
    print(q.get())
    print(q.get())
