import psutil as ps
from typing import NamedTuple
import json

class ProcessEncoder(json.JSONEncoder) :
    def default(self, obj) :
        if isinstance(obj, Process) :
            return obj.pid, obj.name, obj.mode, obj.arrival_time, obj.burst_time
        else :
            return super().default(obj)

class Process(NamedTuple):
    pid: int
    name: str
    mode: str
    arrival_time: str
    burst_time: float


def get_processes() :
    data = {}
    first_epoch = None
    prev_time = 0
    process_gen = ps.process_iter(
        [
            "pid",
            "name",
            "create_time"
        ]
    )
    for process in process_gen :        
        first_epoch = process.info['create_time'] if first_epoch == None else first_epoch
        pid = process.info['pid']
        name = process.info['name']
        arrival_time = round(process.info['create_time'] - first_epoch, 3)
        mode = 'root' if (name == 'root') else 'user'
        burst_time = round(arrival_time - prev_time , 5)
        
        if burst_time != 0 :
            p = Process(pid, name, mode, arrival_time, burst_time )
            data[p.pid] = p
            prev_time = arrival_time
            

    ### saving data in a json file
    with open('./process_info.json', 'w') as file :            
        json.dump(data, file, cls=ProcessEncoder) 

get_processes()
