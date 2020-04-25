from gurobipy import *
from tabulate import tabulate

from Model.Network import Network


def run():
    try:
        f = open("./data2.dat", "r")
        model = Model("Edge Computing Resource Allocation")
        network = Network(model)

        N = int(f.readline())

        for i in range(N):
            l = f.readline()
            node_data = l.split(",")
            network.add_new_random_node(node_data[0],node_data[1],node_data[2],node_data[3])

        set_objectives(network)
        set_eq_constraints(network)
        set_unq_constraints(network)

        model.setParam("NonConvex", 2)
        model.setParam("MIPGap", 0.07)

        model.write("log.lp")
        model.optimize()

        print_result(network,N)

    except GurobiError as e:
        print('Error code ' + str(e.errno) + ": " + str(e))

    except AttributeError as e:
        print('Encountered an attribute error')


def set_objectives(network: Network):
    network.model.setObjectiveN(quicksum(network.nodes[i].total_time for i in range(network.get_size())), 1)
    network.model.setObjectiveN(quicksum(network.nodes[i].total_energy for i in range(network.get_size())),
                                2)


def set_eq_constraints(network: Network):
    model = network.model
    for i in range(network.get_size()):
        node = network.nodes[i]
        model.addConstr(node.local_time == ((1 - node.x) * node.task_size) / node.cpu_power)
        model.addConstr(node.transmit_time * node.transmit_rate == node.x * node.data_size)
        model.addConstr(node.edge_time * node.edge_cpu == node.x * node.task_size)

        model.addConstr(node.interference == quicksum(network.nodes[j].x * network.nodes[j].transmit_power
                                                      * (node.distance(0, 0) ** -2) for j in range(network.get_size())
                                                      if j != i)
                        + network.noise)
        model.addConstr(node.signal_power == node.x * node.transmit_power * (node.distance(0, 0) ** 2))
        model.addConstr(node.signal_power >= node.interference * network.theta)
        model.addConstr(node.signal_power_plus == node.signal_power + 1)
        model.addGenConstrLogA(node.signal_power_plus, node.maximum_rate, 2)

        model.addConstr(node.local_energy == node.task_size * node.cpu_power*node.cpu_power*network.k*(1-node.x))
        model.addConstr(node.edge_energy == node.transmit_power * node.transmit_time)
        model.addConstr(node.total_energy == node.x * node.edge_energy + (1 - node.x) * node.local_energy)
        model.addConstr(quicksum(network.nodes[i].x for i in range(network.get_size())) == network.used_channels)


def set_unq_constraints(network: Network):
    model = network.model
    for i in range(network.get_size()):
        node = network.nodes[i]
        model.addConstr(node.total_time >= node.edge_time + node.transmit_time)
        model.addConstr(node.total_time >= node.local_time)
        model.addConstr(node.transmit_rate*network.used_channels <= node.maximum_rate * 2 * network.bandwidth)
        model.addConstr(node.transmit_power >= node.min_power )
        model.addConstr(node.transmit_power <= node.max_power)
    model.addConstr(network.used_channels <= network.max_channels)
    model.addConstr(quicksum(network.nodes[i].edge_cpu * network.nodes[i].x
                             for i in range(network.get_size())) <= network.max_cpu)


def print_result(network: Network,N):
    result = []
    for i in range(network.get_size()):
        result.append(network.nodes[i].get_result())

    m = network.model
    nSolutions = m.SolCount
    nObjectives = m.NumObj
    print('Problem has', nObjectives, 'objectives')
    print('Gurobi found', nSolutions, 'solutions')
    print(tabulate(result, headers=['index', 'x', 'time', 'energy', 'cpu', 'rate', 'power',
                                    'edge time', 'local time', 'transmit time','edge time',
                                    'Signal Power', 'data size', 'task size', 'maximum rate','distance','interference']))
    m.params.SolutionNumber = 0
    m.params.ObjNumber = 1
    print(' ', m.ObjNVal/N, end='')
    m.params.ObjNumber = 2
    print(' ', m.ObjNVal/N, end='')



run()
