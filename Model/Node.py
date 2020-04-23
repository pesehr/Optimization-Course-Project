from gurobipy import *


class Node:

    def __init__(self, data_size, location, task_size, max_power, min_power, cpu_power, gurobi_model, index):
        self.data_size = data_size
        self.location = location
        self.task_size = task_size
        self.max_power = max_power
        self.min_power = min_power
        self.cpu_power = cpu_power

        self.total_time = gurobi_model.addVar(vtype=GRB.CONTINUOUS, name="t" + index)
        self.local_time = gurobi_model.addVar(vtype=GRB.CONTINUOUS, name="t_l" + index)
        self.edge_time = gurobi_model.addVar(vtype=GRB.CONTINUOUS, name="t_ec" + index)
        self.transmit_time = gurobi_model.addVar(vtype=GRB.CONTINUOUS, name="t_et" + index)

        self.transmit_rate = gurobi_model.addVar(vtype=GRB.CONTINUOUS, name="r" + index)
        self.edge_cpu = gurobi_model.addVar(vtype=GRB.CONTINUOUS, name="f" + index)
        self.maximum_rate = gurobi_model.addVar(vtype=GRB.CONTINUOUS, name="mr" + index)
        self.interference = gurobi_model.addVar(vtype=GRB.CONTINUOUS, name="ir" + index)
        self.transmit_power = gurobi_model.addVar(vtype=GRB.CONTINUOUS, name="p" + index)
        self.signal_power = gurobi_model.addVar(vtype=GRB.CONTINUOUS, name="SINR" + index)

        self.total_energy = gurobi_model.addVar(vtype=GRB.CONTINUOUS, name="e" + index)
        self.local_energy = gurobi_model.addVar(vtype=GRB.CONTINUOUS, name="el" + index)
        self.edge_energy = gurobi_model.addVar(vtype=GRB.CONTINUOUS, name="ee" + index)

        self.x = gurobi_model.addVar(vtype=GRB.BINARY, name="x")
        self.index = index

    def distance(self, x, y):
        return math.sqrt((self.location[0] - x) ** 2 + (self.location[1] - y) ** 2)

    def get_result(self):
        result = [self.index, self.x.x, self.total_time.x, self.total_energy.x, self.edge_cpu.x, self.transmit_rate.x,
                  self.transmit_power.x, self.edge_time.x, self.local_time.x, self.transmit_time.x, self.data_size,
                  self.task_size]
        return result
