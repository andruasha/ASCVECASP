import matplotlib.pyplot as plt
import random

SCALE = 5


class ElectricCircuit:

    def __init__(self, nodes_num, branches_num):

        self.nodes_num = nodes_num
        self.branches_num = branches_num
        self.nodes_connections = {}
        self.contour_points = []
        self.nodes_coords = {}

    def find_near_node(self, node_coords):
        near_nodes = []
        directions = [
            {'x': 5, 'y': 0},
            {'x': -5, 'y': 0},
            {'x': 0, 'y': 5},
            {'x': 0, 'y': -5},
        ]

        for direction in directions:
            target_coords = {'x': node_coords['x'] + direction['x'],
                             'y': node_coords['y'] + direction['y']}
            if target_coords in self.nodes_coords.values():
                key = next((k for k, v in self.nodes_coords.items() if v == target_coords), None)
                if key:
                    near_nodes.append({key: target_coords})

        return near_nodes

    def add_node(self):

        template_two_nodes_1 = {'node1': {'x': 0, 'y': 0},
                                'node2': {'x': SCALE, 'y': 0}}

        template_two_nodes_2 = {'node1': {'x': 0, 'y': 0},
                                'node2': {'x': 0, 'y': SCALE}}

        template_three_nodes_1 = {'node1': {'x': 0, 'y': 0},
                                  'node2': {'x': 0, 'y': SCALE},
                                  'node3': {'x': SCALE, 'y': SCALE}}

        template_three_nodes_2 = {'node1': {'x': 0, 'y': SCALE},
                                  'node2': {'x': SCALE, 'y': SCALE},
                                  'node3': {'x': SCALE, 'y': 0}}

        template_three_nodes_3 = {'node1': {'x': SCALE, 'y': SCALE},
                                  'node2': {'x': SCALE, 'y': 0},
                                  'node3': {'x': 0, 'y': 0}}

        template_four_nodes_1 = {'node1': {'x': 0, 'y': 0},
                                 'node2': {'x': 0, 'y': SCALE},
                                 'node3': {'x': SCALE, 'y': SCALE},
                                 'node4': {'x': SCALE, 'y': 0}}

        template_four_nodes_2 = {'node1': {'x': 0, 'y': SCALE},
                                 'node2': {'x': SCALE, 'y': SCALE},
                                 'node3': {'x': 2 * SCALE, 'y': SCALE},
                                 'node4': {'x': SCALE, 'y': 0}}

        template_four_nodes_3 = {'node1': {'x': 0, 'y': SCALE},
                                 'node2': {'x': SCALE, 'y': 2 * SCALE},
                                 'node3': {'x': SCALE, 'y': SCALE},
                                 'node4': {'x': SCALE, 'y': 0}}

        template_four_nodes_4 = {'node1': {'x': SCALE, 'y': SCALE},
                                 'node2': {'x': 2 * SCALE, 'y': 0},
                                 'node3': {'x': SCALE, 'y': 0},
                                 'node4': {'x': 0, 'y': 0}}

        template_four_nodes_5 = {'node1': {'x': 0, 'y': 0},
                                 'node2': {'x': 0, 'y': SCALE},
                                 'node3': {'x': 0, 'y': 2 * SCALE},
                                 'node4': {'x': SCALE, 'y': SCALE}}

        if self.nodes_num == 2:
            self.nodes_coords = random.choice([template_two_nodes_1,
                                               template_two_nodes_2])

        if self.nodes_num == 3:
            self.nodes_coords = random.choice([template_three_nodes_1,
                                               template_three_nodes_2,
                                               template_three_nodes_3])

        if self.nodes_num == 4:
            self.nodes_coords = random.choice([template_four_nodes_1,
                                               template_four_nodes_2,
                                               template_four_nodes_3,
                                               template_four_nodes_4,
                                               template_four_nodes_5])

    def create_nodes_connections(self):
        for node, coords in self.nodes_coords.items():
            near_nodes = self.find_near_node(coords)
            for near_node in near_nodes:
                for key, value in near_node.items():
                    if (((node + '->' + key) not in self.nodes_connections) and
                            ((key + '->' + node) not in self.nodes_connections)):
                        self.nodes_connections[node + '->' + key] = [[coords, value]]

    def get_num_of_connected_nodes(self, target_node):
        connected_nodes = []

        for key in self.nodes_connections.keys():
            if target_node in key.split('->'):
                connected_nodes.append((set(key.split('->')) - {target_node}).pop())

        return connected_nodes

    def visualise_circuit(self):
        plt.figure(figsize=(5, 5))
        plt.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray')
        plt.xticks(range(-13, 14, 1))
        plt.yticks(range(-13, 14, 1))
        plt.xlim(-13, 13)
        plt.ylim(-13, 13)
        plt.axis('equal')

        for node, coords in self.nodes_coords.items():
            plt.plot(coords['x'], coords['y'], 'ko')

        for key, value in self.nodes_connections.items():
            for connection in value:
                for i in range(0, len(connection)):
                    if i + 1 < len(connection):
                        plt.plot([connection[i]['x'], connection[i + 1]['x']],
                                 [connection[i]['y'], connection[i + 1]['y']], 'k-')
        plt.show()

    def get_coords_by_node(self, node):
        for key, value in self.nodes_coords.items():
            if key == node:
                return value

    def check_exist_node(self, target_coords):
        for name, coords in self.nodes_coords.items():
            if coords == target_coords:
                return True
        return False

    @staticmethod
    def get_node_name(target_node):
        return list(target_node.keys())[0]

    @staticmethod
    def get_node_coords(target_node):
        return list(target_node.values())[0]
