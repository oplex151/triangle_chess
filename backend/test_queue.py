import queue
import threading
from global_var import *

def view():
    global match_queue
    while(1):
        input()
        print(match_queue.qsize())


threading.Thread(target=view).start()
if __name__ == '__main__':
    match_queue.put(1)
    match_queue.put(2)
    while(1):
        1