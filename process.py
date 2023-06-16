import psutil as ps
import json
from dataclasses import dataclass

class ProcessEncoder(json.JSONEncoder) :
    def default(self, obj) :
        if isinstance(obj, Process) :
            return obj.pid, obj.name, obj.mode, obj.arrival_time, obj.burst_time
        else :
            return super().default(obj)

@dataclass
class Process:
    pid: int
    name: str
    mode: str
    arrival_time: str
    burst_time: float


def fetch_process() :
    data = {}
    first_epoch = None
    prev_time = 0
    process_gen = ps.process_iter(
        [
            "pid",
            "name",
            "create_time",
            "username",
            "cpu_times"
        ]
    )
    for process in process_gen :      
        first_epoch = process.info['create_time'] if first_epoch==None else first_epoch
        pid = process.info['pid']
        name = process.info['name']
        arrival_time = round(process.info['create_time'] - first_epoch, 3)
        mode = 'root' if (process.info["username"] == 'root') else 'user'  
        cpu_times = process.info['cpu_times']
        if cpu_times is not None :
            burst_time = cpu_times.user + cpu_times.system
        else :
            burst_time = None
                     # the 0 burst time can have multiple reasons,
                     # like very very short burst time close to 0
                     # or some of them are already finished before 
                     # fetching them. for fixing this problem we use :
                     # burst time = arrival time of the next process - arrival time of this process 
        p = Process(pid, name, mode, arrival_time, burst_time )
        data[p.pid] = p

    # second iteration for processes with 0 burst time :
    data = dict(
        sorted(data.items(), key=lambda x: x[1].arrival_time)
    ) # sorting the data based on arrival time of each process
    for index, process in enumerate(data.values()) :
        process: Process
        if process.burst_time == None :
            if index == len(data)-1 : # the last process
                pass # we cant do anything for this process, so we let it be ...
            else :
                next_process: Process = list(data.values())[index+1]
                burst_time = next_process.arrival_time - process.arrival_time
                process.burst_time = burst_time if burst_time != 0 else 0.001 # some processes have such little burst time 
                                                                              # that it doesn't counted, and some of them
                                                                              # arrive simultaneously, at the end if the 
                                                                              # burst time is still 0, we set it to 0.001

        # data[process.pid] = process
            
    ### saving data in a json file
    with open('./process_info.json', 'w') as file :            
        json.dump(data, file, cls=ProcessEncoder) 
