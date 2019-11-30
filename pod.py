import task

class Pod(object):
    def __init__(self, task):
        self.submit_time = task.submit_time
        self.cpu_capacity = task.cpu_capacity
        self.memory_capacity = task.memory_capacity
        self.disk_capacity = task.disk_capacity
        self.task_duration = task.task_duration
        self.task_execution_time = 0.
    
    def run(self):
        self.task_execution_time = 0.
    
    def timespan(self, time = 16):
        self.task_execution_time += time
        if self.task_duration <= self.task_execution_time:
            return True
        else:
            return False

    