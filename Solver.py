from gurobipy import *
from tabulate import tabulate
from Model.Network import Network


def run():
    try:
        N = 2
        model = Model("Edge Computing Resource Allocation")
        network = Network(model)

        for i in range(N):
            network.add_new_random_node()

        set_objectives(network)
        set_eq_constraints(network)
        set_unq_constraints(network)

        model.setParam("NonConvex", 2)

        model.write("log.lp")
        model.optimize()

        print_result(network)

    except GurobiError as e:
        print('Error code ' + str(e.errno) + ": " + str(e))

    except AttributeError as e:
        print('Encountered an attribute error')


def set_objectives(network: Network):
    network.model.setObjectiveN(quicksum(network.nodes[i].total_time for i in range(network.get_size())), GRB.MINIMIZE)
    # network.model.setObjectiveN(quicksum(network.nodes[i].total_energy for i in range(network.get_size())),
    #                             GRB.MINIMIZE)


def set_eq_constraints(network: Network):
    model = network.model
    for i in range(network.get_size()):
        node = network.nodes[i]
        model.addConstr(node.local_time == ((1 - node.x) * node.task_size) / node.cpu_power)
        model.addConstr(node.transmit_time * node.transmit_rate == node.x * node.data_size)
        model.addConstr(node.edge_time * node.edge_cpu == node.x * node.task_size)

        model.addConstr(node.interference == quicksum(network.nodes[j].x * network.nodes[j].transmit_power
                        * (node.distance(0,0)**-2) for j in range(network.get_size()) if j != i)
                        + network.noise)
        model.addConstr(node.signal_power * node.interference - node.transmit_power * (node.distance(0,0)**2)
                        == node.interference)
        model.addGenConstrLogA(node.signal_power, node.maximum_rate, 2)

        model.addConstr(node.local_energy == node.cpu_power*node.cpu_power*network.etha*node.task_size)
        model.addConstr(node.edge_energy == node.transmit_power * node.data_size*node.transmit_time)
        model.addConstr(node.total_energy == node.x * node.edge_energy + (1-node.x) * node.local_energy)

        model.addConstr(node.x == 1)

def set_unq_constraints(network: Network):
    model = network.model
    for i in range(network.get_size()):
        node = network.nodes[i]
        model.addConstr(node.total_time >= node.edge_time + node.transmit_time)
        model.addConstr(node.total_time >= node.local_time)
        model.addConstr(node.transmit_rate <= node.maximum_rate * 2 * network.bandwidth)
        model.addConstr(node.transmit_power >= node.min_power)
        model.addConstr(node.transmit_power <= node.max_power)
    model.addConstr(quicksum(network.nodes[i].edge_cpu for i in range(network.get_size())) <= network.max_cpu)

def print_result(network :Network):
    # for v in model.getVars():
    #     print('%s %g' % (v.varName, v.x))
    result = []
    for i in range(network.get_size()):
        result.append(network.nodes[i].get_result())
    print(tabulate(result, headers=['index', 'x', 'time', 'energy', 'cpu', 'rate', 'power',
                                    'edge time','local time','transmit time','data size']))


run()
