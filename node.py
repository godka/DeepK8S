import numpy as np
import pod
MAX_CPU_NUM = 12
MAX_MEM = 48
class Node(object):
    def __init__(self):
        self.cpu_max = np.random.randint(1, MAX_CPU_NUM) * 8
        self.memory_max = np.random.randint(1, MAX_MEM) * 8
        self.disk_max = 500.
        self.cpu = 0.
        self.memory = 0.
        self.disk = 0.
        #stable
        self.task_instances = []

    def append(self, task_instance):
        self.cpu += task_instance.cpu_capacity
        self.memory += task_instance.memory_capacity
        self.disk += task_instance.disk_capacity
        pod_ = pod.Pod(task_instance)
        pod_.run()
        self.task_instances.append(pod_)

    def done(self, task_instance):
        self.cpu -= task_instance.cpu_capacity
        self.memory -= task_instance.memory_capacity
        self.disk -= task_instance.disk_capacity
        self.task_instances.remove(task_instance)

    def available(self, task):
        return self.cpu_max >= task.cpu_capacity and \
               self.memory_max >= task.memory_capacity and \
               self.disk_max >= task.disk_capacity
    
    def run(self, forward_time = 16):
        for p in self.task_instances:
            if p.timespan(forward_time):
                self.done(p)
    
    def get_status(self):
        return [self.cpu / self.cpu_max, self.memory / self.memory_max]

