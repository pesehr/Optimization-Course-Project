import random
from typing import List
from gurobipy import *
from Model.Node import Node


class Network:
    nodes = List[Node]

    def __init__(self, model):
        self.max_cpu = 10 ** 10  # 10GHz
        self.bandwidth = 2*(10**7) #29 MHz
        self.max_channels = 10
        self.noise = 10 ** -9  # -100db
        self.model = model
        self.nodes = []
        self.k = 5 * (10 ** -27)
        self.used_channels = model.addVar(vtype=GRB.CONTINUOUS, name="uc")

    def add_new_random_node(self):
        data = random.randint(10 ** 7, 5 * 10 ** 8)
        data = 10 ** 7
        task = random.randint(10 ** 9, 10 ** 12)
        task = 10 ** 10
        # location = [random.randint(10,100),random(10,100)]
        max_power = 0.1
        min_power = 0.001
        cpu_power = 10 ** 9  # 1GHz

        self.nodes.append(
            Node(data, [10, 10], task, max_power, min_power, cpu_power, self.model, str(self.get_size() + 1)))

    def get_size(self):
        return len(self.nodes)
