import numpy as np
from node import Node
from task import TaskCollection
RANDOM_SEED = 42
MAX_NODE_NUM = 1000

class Env:
    def __init__(self, random_seed=RANDOM_SEED):
        np.random.seed(random_seed)
        self.node_list = []
        self.task_collector = None
        self.task_buffer = []
        # 16ms, limit cpu tickcount
        self.base_time = 16
        self.last_state = None
        self.act_time = 0.

    def _now(self):
        return self.act_time

    def reset(self):
        self.act_time = 0.
        node_num = np.random.randint(10, MAX_NODE_NUM)
        for _ in range(node_num):
            self.node_list.append(Node())
        self.task_collector = TaskCollection()
        while len(self.task_buffer) == 0:
            self.tasks, _ = self.task_collector.get_tasks(self.act_time)
            for task in self.tasks:
                self.task_buffer.append(task)
            self.act_time += self.base_time * np.random.rand()
        state, node_idx = [], []
        info = {}
        for t in self.task_buffer:
            for node in self.node_list:
                if node.available(task):
                    state.append(node.get_status() + t.get_status())
            state.append([-1., -1.] + t.get_status())

        for idx, node in enumerate(self.node_list):
            if node.available(self.task_buffer[0]):
                node_idx.append(idx)
        info['idx'] = node_idx

        return state, info

    def step(self, action):
        selected_task = self.task_buffer[0]
        self.task_buffer.pop(0)
        selected_node = action
        if selected_node < 0:
            self.task_buffer.append(selected_task)
            reward = 0.
        else:
            self.node_list[selected_node].append(selected_task)
            reward = self.act_time - selected_task.submit_time # + selected_task.task_duration
            # reward /= 1000.
        done = False
        while len(self.task_buffer) == 0:
            self.tasks, done = self.task_collector.get_tasks(self.act_time)
            if done:
                break
            for task in self.tasks:
                self.task_buffer.append(task)
            forward_time = self.base_time * np.random.rand()
            for p in self.node_list:
                p.run(forward_time)
            self.act_time += forward_time
        state, node_idx = [], []
        info = {}
        for task in self.task_buffer:
            for node in self.node_list:
                if node.available(task):
                    state.append(node.get_status() + task.get_status())
            state.append([-1., -1.] + task.get_status())

        for idx, node in enumerate(self.node_list):
            if node.available(self.task_buffer[0]):
                node_idx.append(idx)
        node_idx.append(-1)
        info['idx'] = node_idx

        return state, reward, done, info

if __name__ == "__main__":
    env = Env()
    obs, info = env.reset()
    while True:
        node_idx = info['idx']
        selected_idx = np.random.randint(len(node_idx))
        obs, rew, done, info = env.step(node_idx[selected_idx])
        print(rew)
        # print(obs[0])
        if done:
            break