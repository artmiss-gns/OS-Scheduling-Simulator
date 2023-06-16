from queue import deque
from process import Process

class SJF :
    def __init__(self, queue: deque) :
        self.queue = queue 
        self.average_wating_time = 0
        self.average_turnaround_time = 0
        self.throughput = 0
        self.utilization = 0
        self.sum_burst_time = 0
        self.count_processes = 0

    def SJF_algorithm(self) :
        # the queue is already sorted by arrival time
        
        start_time = 0
        current_time = 0
        while len(self.queue) :
          
            current_process = self.queue.popleft()
            current_process: Process
            
            if (x := (current_time - current_process.arrival_time) ) >= 0 :
                self.average_wating_time += x
            else : # if the process is after current time
                current_time = current_process.arrival_time
                pass
            
            self.sum_burst_time += current_process.burst_time
            current_time += current_process.burst_time
            self.count_processes += 1
            
            yield current_process
        
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