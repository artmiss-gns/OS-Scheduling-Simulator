import psutil as ps
from typing import NamedTuple

class Process(NamedTuple):
    pid: int
    name: str
    mode: str
    arrival_time: str
    burst_time: float


def main() :
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
            prev_time = arrival_time
            print(p)


if __name__ == "__main__" :
    main() 
    
