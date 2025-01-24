from conf.config import SCALE

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random


class ElectricCircuit:

    def __init__(self, branches_num, nodes):

        self.nodes = nodes
        self.nodes_num = len(nodes)
        self.nodes_connections = {}
        self.branches_num = branches_num

    def find_near_node(self, nodes):
        near_nodes = []
        directions = [
            {'x': SCALE, 'y': 0},
            {'x': -SCALE, 'y': 0},
            {'x': 0, 'y': SCALE},
            {'x': 0, 'y': -SCALE}
        ]

        for direction in directions:
            target_coords = {'x': nodes['x'] + direction['x'],
                             'y': nodes['y'] + direction['y']}
            if target_coords in self.nodes.values():
                key = next((k for k, v in self.nodes.items() if v == target_coords), None)
                if key:
                    near_nodes.append({key: target_coords})

        return near_nodes

    def create_nodes_connections(self):
        def generate_neighbour_coords(node_coords, scale):
            return {
                'left': {'x': node_coords['x'] - scale, 'y': node_coords['y']},
                'upper_left': {'x': node_coords['x'] - scale, 'y': node_coords['y'] + scale},
                'upper': {'x': node_coords['x'], 'y': node_coords['y'] + scale},
                'upper_right': {'x': node_coords['x'] + scale, 'y': node_coords['y'] + scale},
                'right': {'x': node_coords['x'] + scale, 'y': node_coords['y']},
                'down_right': {'x': node_coords['x'] + scale, 'y': node_coords['y'] - scale},
                'down': {'x': node_coords['x'], 'y': node_coords['y'] - scale},
                'down_left': {'x': node_coords['x'] - scale, 'y': node_coords['y'] - scale},
            }

        def add_connection_if_needed(coord1, coord2, missing_coord, key_prefix):
            if (self.check_exist_node(coord1) and
                    self.check_exist_node(coord2) and
                    not self.check_exist_node(missing_coord)):
                node1 = self.get_name_by_coords(coord1)
                node2 = self.get_name_by_coords(coord2)
                connection_key = f"{node1}->{node2}"
                if connection_key not in self.nodes_connections:
                    self.nodes_connections[connection_key] = [[coord1, missing_coord, coord2]]

        for node_name, node_coords in self.nodes.items():
            near_nodes = self.find_near_node(node_coords)
            for near_node in near_nodes:
                for key, value in near_node.items():
                    connection_key = f"{node_name}->{key}"
                    reverse_key = f"{key}->{node_name}"
                    if connection_key not in self.nodes_connections and reverse_key not in self.nodes_connections:
                        self.nodes_connections[connection_key] = [[node_coords, value]]

            neighbours = generate_neighbour_coords(node_coords, SCALE)

            add_connection_if_needed(neighbours['left'], neighbours['upper'],
                                     neighbours['upper_left'], "ul")
            add_connection_if_needed(neighbours['upper'], neighbours['right'],
                                     neighbours['upper_right'], "ur")
            add_connection_if_needed(neighbours['right'], neighbours['down'],
                                     neighbours['down_right'], "dr")
            add_connection_if_needed(neighbours['down'], neighbours['left'],
                                     neighbours['down_left'], "dl")

        if self.nodes_num == 2:
            self.nodes_connections['node1->node2'].append([{'x': 0, 'y': 0},
                                                           {'x': 0, 'y': 0.5*SCALE},
                                                           {'x': SCALE, 'y': 0.5*SCALE},
                                                           {'x': SCALE, 'y': 0}])

            self.nodes_connections['node1->node2'].append([{'x': 0, 'y': 0},
                                                           {'x': 0, 'y': -0.5*SCALE},
                                                           {'x': SCALE, 'y': -0.5*SCALE},
                                                           {'x': SCALE, 'y': 0}])

            available_connections = [
                {'node1->node2': [{'x': 0, 'y': 0},
                                  {'x': 0, 'y': SCALE},
                                  {'x': SCALE, 'y': SCALE},
                                  {'x': SCALE, 'y': 0}]},

                {'node1->node2': [{'x': 0, 'y': 0},
                                  {'x': 0, 'y': -SCALE},
                                  {'x': SCALE, 'y': -SCALE},
                                  {'x': SCALE, 'y': 0}]},

                {'node1->node2': [{'x': 0, 'y': 0},
                                  {'x': 0, 'y': 1.5*SCALE},
                                  {'x': SCALE, 'y': 1.5*SCALE},
                                  {'x': SCALE, 'y': 0}]},
            ]

            for available_connection in available_connections:
                if self.get_num_branches() < self.branches_num:
                    for key, value in available_connection.items():
                        self.nodes_connections[key].append(value)
                else:
                    break

        if self.nodes_num == 3:
            available_connections_stage_1 = [
                {'node1->node2': [{'x': 0, 'y': 0},
                                  {'x': -0.5*SCALE, 'y': 0},
                                  {'x': -0.5*SCALE, 'y': SCALE},
                                  {'x': 0, 'y': SCALE}]},

                {'node2->node3': [{'x': 0, 'y': SCALE},
                                  {'x': 0, 'y': 1.5*SCALE},
                                  {'x': SCALE, 'y': 1.5*SCALE},
                                  {'x': SCALE, 'y': SCALE}]},

                {'node3->node1': [{'x': SCALE, 'y': SCALE},
                                  {'x': 1.5*SCALE, 'y': SCALE},
                                  {'x': 1.5*SCALE, 'y': -0.5*SCALE},
                                  {'x': 0, 'y': -0.5*SCALE},
                                  {'x': 0, 'y': 0}]}
            ]

            for available_connection in self.get_random_elements(available_connections_stage_1, 2):
                if self.get_num_branches() < self.branches_num:
                    for key, value in available_connection.items():
                        self.nodes_connections[key].append(value)
                else:
                    break

    def get_num_of_connected_nodes(self, target_node):
        connected_nodes = []

        for node_connection in self.nodes_connections.keys():
            if target_node in node_connection.split('->'):
                connected_nodes.append((set(node_connection.split('->')) - {target_node}).pop())

        return connected_nodes

    def visualise_circuit(self):
        plt.figure(figsize=(5, 5))
        plt.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray')
        plt.xticks(range(-13, 14, 1))
        plt.yticks(range(-13, 14, 1))
        plt.xlim(-13, 13)
        plt.ylim(-13, 13)
        # plt.axis('equal')

        for node, coords in self.nodes.items():
            plt.plot(coords['x'], coords['y'], 'ko')

        for key, value in self.nodes_connections.items():
            for connection in value:
                for i in range(0, len(connection)):
                    if i + 1 < len(connection):
                        plt.plot([connection[i]['x'], connection[i + 1]['x']],
                                 [connection[i]['y'], connection[i + 1]['y']], 'k-')

        plt.show()

    def get_coords_by_name(self, node_name):
        for key, value in self.nodes.items():
            if key == node_name:
                return value

    def get_name_by_coords(self, node_coords):
        for key, value in self.nodes.items():
            if value == node_coords:
                return key

    def check_exist_node(self, target_coords):
        for name, coords in self.nodes.items():
            if coords == target_coords:
                return True
        return False

    def get_num_branches(self):
        num_branches = 0
        for key, value in self.nodes_connections.items():
            num_branches = num_branches + len(value)
        return num_branches

    @staticmethod
    def get_node_name(target_node):
        return list(target_node.keys())[0]

    @staticmethod
    def get_node_coords(target_node):
        return list(target_node.values())[0]

    @staticmethod
    def get_random_elements(elements_array, elements_num):
        return random.sample(elements_array, elements_num)
