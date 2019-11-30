import numpy as np
import collections

class Task(object):
    def __init__(self, submit_time, cpu_capacity, memory_capacity, disk_capacity, duration):
        self.submit_time = submit_time
        self.cpu_capacity = cpu_capacity
        self.memory_capacity = memory_capacity
        self.disk_capacity = disk_capacity
        self.task_duration = duration
    
    def get_status(self):
        return [self.submit_time,
            self.cpu_capacity,
            self.memory_capacity,
            self.disk_capacity,
            self.task_duration]
        
class TaskCollection(object):
    def __init__(self, filename = 'jobs-sort.csv'):
        self.filename = filename
        self.trace_arr = []
        self.trace_idx = 0
        self.read_file()
    
    def read_file(self):
        f = open(self.filename, 'r')
        for line in f:
            #id,submit_time,duration,cpu,memory,job_id,task_id,instances_num,disk
            sp = line.split(',')
            submit_time = float(sp[1]) * 1000.
            duration = float(sp[2]) * 1000.
            cpu = float(sp[3])
            # the largest memory cap in ali
            memory = float(sp[4]) * 384.
            disk = float(sp[5])
            _Task = Task(submit_time, cpu, memory, disk, duration)
            self.trace_arr.append(_Task)
        f.close()

    def get_tasks(self, timestamp):
        ready_task = []
        done = False
        while True:
            _var = self.trace_arr[self.trace_idx]
            if _var.submit_time <= timestamp:
                ready_task.append(_var)
            else:
                break
            self.trace_idx += 1
            if self.trace_idx == len(self.trace_arr):
                done = True
                break
        return ready_task, done

def sortedDictValues3(adict): 
    keys = adict.keys() 
    keys.sort() 
    return [adict[key] for key in keys]

if __name__ == "__main__":
    f = open('jobs.csv', 'r')
    jobs_dict = {}
    for line in f:
        #id,submit_time,duration,cpu,memory,job_id,task_id,instances_num,disk
        sp = line.split(',')
        submit_time = float(sp[1])
        duration = float(sp[2])
        cpu = float(sp[3])
        memory = float(sp[4])
        disk = float(sp[-1])
        _Task = Task(submit_time, cpu, memory, disk, duration)
        if submit_time not in jobs_dict:
            jobs_dict[submit_time] = []
        jobs_dict[submit_time].append(_Task)
    f.close()
    jobs_dict = collections.OrderedDict(sorted(jobs_dict.items()))
    f = open('jobs-sort.csv', 'w')
    idx = 0
    for s_t, Tasks in jobs_dict.items():
        for Task in Tasks:
            f.write(str(idx) + ',' + str(Task.submit_time) + ',' + str(Task.task_duration) + \
                ',' + str(Task.cpu_capacity) + ',' + str(Task.memory_capacity) + ',' + str(Task.disk_capacity))
            f.write('\n')
            idx += 1
    f.close()
