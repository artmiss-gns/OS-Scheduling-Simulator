from queue import deque
from process import Process
import time

class RR :
    def __init__(self, queue: deque, *, quantum_time=None) :
        self.queue = queue 
        self.quantum_time = quantum_time
        self.average_wating_time = 0
        self.average_turnaround_time = 0
        self.throughput = 0
        self.utilization = 0
        self.sum_burst_time = 0
        self.count_processes = 0

    def RR_algorithm(self) :
        # the queue is already sorted by arrival time
        
        start_time = 0
        current_time = 0
        while len(self.queue) :
          
            current_process = self.queue.popleft()
            current_process: Process
            current_time = current_process.arrival_time if current_time == 0 else current_time
            
            # setting an adaptive quantum time if it is not given in arguments
            self.quantum_time = min(
                current_process.burst_time, max(0.2, round(current_process.burst_time / 2))
            )
            
            if (x := (current_time - current_process.arrival_time) ) >= 0 :
                self.average_wating_time += x
            else : # if the process is after current time
                current_time = current_process.arrival_time
                pass
            
            
            if current_process.burst_time <= self.quantum_time :
                self.sum_burst_time += current_process.burst_time
                current_time += current_process.burst_time
                self.count_processes += 1
                yield current_process
            else :
                self.average_wating_time -= ( (current_time - current_process.arrival_time) - self.quantum_time )
                current_process.burst_time -= self.quantum_time
                current_time += current_process.burst_time
                self.sum_burst_time += current_process.burst_time
                self.queue.append(current_process)
        
        end_time = current_process.arrival_time + current_process.burst_time
        self.average_wating_time = (self.average_wating_time) / self.count_processes
        self.average_turnaround_time = self.average_wating_time + (self.sum_burst_time / self.count_processes)
        self.throughput = self.count_processes / end_time
        self.utilization = self.sum_burst_time / end_time
        
    def get_info(self) :
        return {
            'average_wating_time': self.average_wating_time,
            'average_turnaround_time': self.average_turnaround_time,
            'throughput': self.throughput,
            'utilization': self.utilization,
        }
    
    
