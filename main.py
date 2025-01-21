from conf.config import SCALE
from src.electric_circuit import ElectricCircuit


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

circuit = ElectricCircuit(4, 0, template_four_nodes_2)

circuit.create_nodes_connections()
circuit.visualise_circuit()
