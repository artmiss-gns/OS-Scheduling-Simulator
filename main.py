from process import Process
from RR import RR
from SJF import SJF
from process import fetch_process

import json 
from queue import deque
from tqdm import tqdm
import time
from prettytable import PrettyTable


def get_processes(*, process_address=None) :    
    class ProcessDecoder(json.JSONDecoder):
        def decode(self, json_str):
            data = super().decode(json_str)
            return [Process(*value) for key, value in data.items()]
    
    if process_address == None :
        fetch_process()  
         
    with open('process_info.json', 'r') as file :   
        processes = json.load(file, cls=ProcessDecoder)
        
    return processes
   
def execute(*,queue, algorithm, progress_bar=True, wate_time=0.05) :
    if progress_bar :
        # progress_bar = get_progress_bar(queue, algorithm, wate_time)    
        progress_bar = get_progress_bar(queue, algorithm)
        for p in progress_bar:
            time.sleep(wate_time)
            progress_bar.set_description(f"Processing pid: {p.pid}")
    else :
        for p in algorithm(queue) :
            print(p)
        
def get_progress_bar(queue, algorithm) :
    progress_bar = tqdm(
        algorithm(), # calling the algorithm
        total=len(queue),
        desc=f"Processing...",
        ncols=100,
        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]",
        position=0,
    )

    return progress_bar
  
def show_processes() :
    processes = get_processes() # you can specify process address here if you want to read from a file
    processes: Process
    
    table = PrettyTable()
    table.field_names = ["PID", "Process Name", "Mode", "Arrival Time", "Burst Time"]

    for process in processes :
        table.add_row(
            [       
            process.pid, 
            process.name, 
            process.mode, 
            round(process.arrival_time, 5),
            round(process.burst_time, 5),
            ]
        )
    print(table)

def menu() :
    print(''' 
        1 -> show processes
        2 -> start the process scheduling
        0 -> exit
        ''')
    
def show_info(alg) :
    table = PrettyTable()
    table.field_names = ["average wating time", "average turnaround time", "throughput", "cpu utilization"]
    table.add_row([
        alg.average_wating_time, 
        alg.average_turnaround_time, 
        alg.throughput, 
        alg.utilization, 
    ])
    print(table)

def main() :
    '''
        MLQ
            root queue --> RR
            user queue --> SJF
    '''
    wate_time = float(input("wate time: [0.005]") or 0.005) # getting the wate time from the user, if ti's empty the
                                                     # default value will be set which is 0.005
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
    rr = RR(root_queue, quantum_time=0.2)
    sjf = SJF(user_queue)
    execute(queue=rr.queue, algorithm=rr.RR_algorithm, progress_bar=True, wate_time=wate_time)
    execute(queue=sjf.queue, algorithm=sjf.SJF_algorithm, progress_bar=True, wate_time=wate_time)
    
    
    ### showing the results :
    print("\nRR: ")
    show_info(rr)
    
    print("\nSJF: ")
    show_info(sjf)
    
    print("\n\nIf throughput and cpu utilization is so low, the reason could be due to a very large arrival time of some processes\n")
    
if __name__ == "__main__" :
    menu()
    
    while (option := input("Choose an option: ")) :
        print()
        
        if option == '1' :
            show_processes()
            
        elif option == "2" :
            main()
            
        else :
            break