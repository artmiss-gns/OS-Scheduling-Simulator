from queue import deque
from process import Process

def SJF_algorithm(queue: deque) :
    queue = deque(sorted(queue, key=lambda p: p.burst_time))
    while len(queue) :
        current_process = queue.popleft()
        current_process: Process
        yield current_process

    
    