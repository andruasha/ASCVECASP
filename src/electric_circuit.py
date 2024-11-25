import matplotlib.pyplot as plt
import random


class ElectricCircuit:

    def __init__(self, nodes_num, branches_num):
        self.nodes_num = nodes_num
        self.branches_num = branches_num
        self.nodes_coords = {'node1': {'x': 0, 'y': 0},
                             'node2': {'x': 5, 'y': 0},
                             'node3': {'x': 5, 'y': -5}}
        self.nodes_connections = {}

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

    def connect_nodes(self):
        plt.figure(figsize=(10, 10))
        plt.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray')
        plt.xticks(range(-13, 14, 1))
        plt.yticks(range(-13, 14, 1))
        plt.xlim(-13, 13)
        plt.ylim(-13, 13)

        for node in self.nodes_coords.keys():
            self.nodes_connections[node] = []

        for node, coords in self.nodes_coords.items():
            plt.plot(coords['x'], coords['y'], 'ko')
            near_nodes = self.find_near_node(coords)
            for near_node in near_nodes:
                for key, value in near_node.items():
                    if key not in self.nodes_connections[node]:
                        x_coords = [coords['x'], value['x']]
                        y_coords = [coords['y'], value['y']]
                        plt.plot(x_coords, y_coords, 'b-')
                        self.nodes_connections[node].append(key)
        plt.show()

    def get_num_branches(self):
        unique_connections = set()

        for node, connections in self.nodes_connections.items():
            for connected_node in connections:
                unique_connections.add(tuple(sorted([node, connected_node])))

        return len(unique_connections)
