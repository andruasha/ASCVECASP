import matplotlib.pyplot as plt
import random


class ElectricCircuit:

    def __init__(self, nodes_num, branches_num):

        available_init_coords = [
            {'x': 0, 'y': 0},
            {'x': 5, 'y': 0},
            {'x': 0, 'y': -5},
            {'x': 5, 'y': -5}
        ]

        selected_coords = random.sample(available_init_coords, 3)

        self.nodes_num = nodes_num
        self.branches_num = branches_num
        self.nodes_connections = {}
        self.contour_points = []
        self.nodes_coords = {
            f'node{i + 1}': coord for i, coord in enumerate(selected_coords)
        }

    def find_double_nodes(self):
        def check_direction(nodes_coords, target, first_pair, second_pair):
            if target in nodes_coords.values():
                if all(pair not in nodes_coords.values() for pair in first_pair):
                    return random.choice(first_pair)
                if all(pair not in nodes_coords.values() for pair in second_pair):
                    return random.choice(second_pair)
            return None

        for node, coords in self.nodes_coords.items():
            checks = [
                lambda: check_direction(
                    self.nodes_coords, {'x': coords['x'] + 5, 'y': coords['y']},
                    [{'x': coords['x'], 'y': coords['y'] + 5}, {'x': coords['x'] + 5, 'y': coords['y'] + 5}],
                    [{'x': coords['x'], 'y': coords['y'] - 5}, {'x': coords['x'] + 5, 'y': coords['y'] - 5}]
                ),
                lambda: check_direction(
                    self.nodes_coords, {'x': coords['x'] - 5, 'y': coords['y']},
                    [{'x': coords['x'], 'y': coords['y'] + 5}, {'x': coords['x'] - 5, 'y': coords['y'] + 5}],
                    [{'x': coords['x'], 'y': coords['y'] - 5}, {'x': coords['x'] - 5, 'y': coords['y'] - 5}]
                ),
                lambda: check_direction(
                    self.nodes_coords, {'x': coords['x'], 'y': coords['y'] + 5},
                    [{'x': coords['x'] + 5, 'y': coords['y']}, {'x': coords['x'] + 5, 'y': coords['y'] + 5}],
                    [{'x': coords['x'] - 5, 'y': coords['y']}, {'x': coords['x'] - 5, 'y': coords['y'] + 5}]
                ),
                lambda: check_direction(
                    self.nodes_coords, {'x': coords['x'], 'y': coords['y'] - 5},
                    [{'x': coords['x'] + 5, 'y': coords['y']}, {'x': coords['x'] + 5, 'y': coords['y'] - 5}],
                    [{'x': coords['x'] - 5, 'y': coords['y']}, {'x': coords['x'] - 5, 'y': coords['y'] - 5}]
                )
            ]

            random.shuffle(checks)

            for check in checks:
                result = check()
                if result:
                    return result

    def find_right_angle(self):
        def check_condition(nodes_coords, target, cond1, cond2, exclude):
            if target in nodes_coords.values() and cond1 in nodes_coords.values() and exclude not in nodes_coords.values():
                return exclude
            return None

        for node, coords in self.nodes_coords.items():
            checks = [
                lambda: check_condition(
                    self.nodes_coords,
                    {'x': coords['x'] + 5, 'y': coords['y']},
                    {'x': coords['x'], 'y': coords['y'] - 5},
                    None,
                    {'x': coords['x'] + 5, 'y': coords['y'] - 5}
                ),
                lambda: check_condition(
                    self.nodes_coords,
                    {'x': coords['x'] + 5, 'y': coords['y']},
                    {'x': coords['x'], 'y': coords['y'] + 5},
                    None,
                    {'x': coords['x'] + 5, 'y': coords['y'] + 5}
                ),
                lambda: check_condition(
                    self.nodes_coords,
                    {'x': coords['x'] - 5, 'y': coords['y']},
                    {'x': coords['x'], 'y': coords['y'] - 5},
                    None,
                    {'x': coords['x'] - 5, 'y': coords['y'] - 5}
                ),
                lambda: check_condition(
                    self.nodes_coords,
                    {'x': coords['x'] - 5, 'y': coords['y']},
                    {'x': coords['x'], 'y': coords['y'] + 5},
                    None,
                    {'x': coords['x'] - 5, 'y': coords['y'] + 5}
                )
            ]

            random.shuffle(checks)

            for check in checks:
                result = check()
                if result:
                    return result

        return None

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
        nodes_coords_keys = list(self.nodes_coords.keys())
        random.shuffle(nodes_coords_keys)
        self.nodes_coords = {key: self.nodes_coords[key] for key in nodes_coords_keys}
        new_node_coords = self.find_right_angle()

        if not new_node_coords:
            new_node_coords = self.find_double_nodes()

        self.nodes_coords['node' + str(len(self.nodes_coords) + 1)] = new_node_coords

    def create_nodes_connections(self):
        for node, coords in self.nodes_coords.items():
            near_nodes = self.find_near_node(coords)
            for near_node in near_nodes:
                for key, value in near_node.items():
                    if (((node + '->' + key) not in self.nodes_connections) and
                            ((key + '->' + node) not in self.nodes_connections)):
                        self.nodes_connections[node+'->'+key] = [coords, value]

        single_nodes = self.get_single_nodes()
        third_node_coords = {}
        imaginary_node_coords = {}

        if len(single_nodes) == 2:
            for node, coords in self.nodes_coords.items():
                if node not in single_nodes.keys():
                    third_node_coords = coords
            keys = list(single_nodes.keys())
            values = list(single_nodes.values())
            imaginary_node_coords = {'x': values[0]['x'] + values[1]['x'] - third_node_coords['x'],
                                     'y': values[0]['y'] + values[1]['y'] - third_node_coords['y']}
            self.nodes_connections[keys[0] + '->' + keys[1]] = [values[0], imaginary_node_coords, values[1]]

    def get_num_of_connected_nodes(self, target_node):
        connected_nodes = []

        for key in self.nodes_connections.keys():
            if target_node in key.split('->'):
                connected_nodes.append((set(key.split('->')) - {target_node}).pop())

        return connected_nodes

    def get_single_nodes(self):
        single_nodes = {}

        for node, coords in self.nodes_coords.items():
            if len(self.get_num_of_connected_nodes(node)) == 1:
                single_nodes[node] = coords

        return single_nodes

    def visualise_circuit(self):
        plt.figure(figsize=(10, 10))
        plt.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray')
        plt.xticks(range(-13, 14, 1))
        plt.yticks(range(-13, 14, 1))
        plt.xlim(-13, 13)
        plt.ylim(-13, 13)

        for node, coords in self.nodes_coords.items():
            plt.plot(coords['x'], coords['y'], 'ko')

        for key, value in self.nodes_connections.items():
            for i in range(0, len(value)):
                if i + 1 < len(value):
                    plt.plot([value[i]['x'], value[i+1]['x']], [value[i]['y'], value[i+1]['y']], 'k-')
        plt.show()

    def get_coords_by_node(self, node):
        for key, value in self.nodes_coords.items():
            if key == node:
                return value
