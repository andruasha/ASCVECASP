import matplotlib.pyplot as plt
from src.electric_circuit import ElectricCircuit
from src.elements_places import ElementsPlacer
from src.visualize_circuit import CircuitVisualize
from conf.config import SCALE


template_two_nodes_1 = {'node1': {'x': 0, 'y': 0},
                        'node2': {'x': SCALE, 'y': 0}}

template_three_nodes_1 = {'node1': {'x': 0, 'y': 0},
                          'node2': {'x': 0, 'y': SCALE},
                          'node3': {'x': SCALE, 'y': SCALE}}

template_four_nodes_1 = {'node1': {'x': 0, 'y': 0},
                         'node2': {'x': 0, 'y': SCALE},
                         'node3': {'x': SCALE, 'y': SCALE},
                         'node4': {'x': SCALE, 'y': 0}}

template_four_nodes_2 = {'node1': {'x': 0, 'y': SCALE},
                         'node2': {'x': SCALE, 'y': SCALE},
                         'node3': {'x': 2 * SCALE, 'y': SCALE},
                         'node4': {'x': SCALE, 'y': 0}}

branches = 10
circuit_topology = ElectricCircuit(branches, template_four_nodes_1)
circuit_topology.create_nodes_connections()

circuit = ElementsPlacer(circuit_topology, 5, 5, 2, 2, 2)
print(circuit.layout)

CircuitVisualize(circuit, circuit_topology).visualize()
