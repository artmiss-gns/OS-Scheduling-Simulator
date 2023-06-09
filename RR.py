from queue import deque
from process import Process

def RR_scheduling(queue: deque, *, quantum_time = 0.2) :
    # the queue is already sorted by arrival time
    while len(queue) :
        current_process = queue.popleft()
        current_process: Process
        
        if current_process.burst_time <= quantum_time :
            yield current_process
        else :
            current_process.burst_time -= quantum_time
            queue.append(current_process)
    
    
