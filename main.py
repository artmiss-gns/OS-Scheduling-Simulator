from process import Process
from RR import RR_algorithm

import json 
from queue import deque
from tqdm import tqdm
import time

def get_processes(process_address='./process_info.json') :    
    class ProcessDecoder(json.JSONDecoder):
        def decode(self, json_str):
            data = super().decode(json_str)
            return [Process(*value) for key, value in data.items()]
        
    with open(process_address, 'r') as file :    
        processes = json.load(file, cls=ProcessDecoder)
    
    return processes
   
def execute(*, queue, algorithm=RR_algorithm, progress_bar=True, wate_time=0.05) :
    if progress_bar :
        # progress_bar = get_progress_bar(queue, algorithm, wate_time)    
        progress_bar = get_progress_bar(queue, algorithm, wate_time=0.5)
        for p in progress_bar:
            time.sleep(wate_time)
            progress_bar.set_description(f"Processing pid: {p.pid}")
    else :
        for p in algorithm(queue) :
            print(p)
        
    
def get_progress_bar(queue, algorithm, wate_time) :
    progress_bar = tqdm(
        algorithm(queue), # calling the algorithm
        total=len(queue),
        desc=f"Processing...",
        ncols=100,
        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]",
        position=0,
        mininterval=wate_time
    )

    return progress_bar
  

def main() :
    '''
        MLQ
            root queue --> RR
            user queue --> SJF
    '''
    processes = get_processes()
    processes = sorted(processes, key=lambda p: p.arrival_time) # sorting the processes based on arrival time
    
    # adding the process to their appropriate queue
    root_queue = deque()
    user_queue = deque()
    for p in processes :
        if p.mode == "root" : # root queue
            root_queue.append(p)
        else : # user queue
            user_queue.append(p)

    # start the scheduling algorithms
    execute(queue=root_queue, algorithm=RR_algorithm, progress_bar=True, wate_time=0.05)
    # execute(user_queue, algorithm=SJF_algorithm, progress_bar=True, wate_time=0.05)
    
        
if __name__ == "__main__" :
    main()