import random
from typing import List

from Model.Node import Node


class Network:
    nodes = List[Node]

    def __init__(self, model):
        self.max_cpu = 1000
        self.etha = 10 ** 8
        self.bandwidth = 100
        self.noise = 10 ** -4
        self.model = model
        self.nodes = []

    def add_new_random_node(self):
        self.nodes.append(
            Node(random.randint(10000, 100000), [10, 10], 10000, 1000, 0.01, 0.01, self.model, str(self.get_size() + 1)))

    def get_size(self):
        return len(self.nodes)
