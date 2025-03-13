from conf.config import SCALE

import matplotlib.pyplot as plt
import random
import secrets
import copy
from itertools import combinations


def get_random_elements(elements_array, elements_num):
    return secrets.SystemRandom().sample(elements_array, elements_num)


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
                key = next((node_name for node_name, node_coords in self.nodes.items() if node_coords == target_coords), None)
                if key:
                    near_nodes.append({key: target_coords})

        return near_nodes

    def create_nodes_connections(self):
        for node_name, node_coords in self.nodes.items():
            near_nodes = self.find_near_node(node_coords)
            for near_node in near_nodes:
                for key, value in near_node.items():
                    if (((node_name + '->' + key) not in self.nodes_connections) and
                            ((key + '->' + node_name) not in self.nodes_connections)):
                        self.nodes_connections[node_name + '->' + key] = [[node_coords, value]]

        for node_name, node_coords in self.nodes.items():

            left_neighbour_coords = {'x': node_coords['x'] - SCALE, 'y': node_coords['y']}
            upper_left_neighbour_coords = {'x': node_coords['x'] - SCALE, 'y': node_coords['y'] + SCALE}
            upper_neighbour_coords = {'x': node_coords['x'], 'y': node_coords['y'] + SCALE}
            upper_right_neighbour_coords = {'x': node_coords['x'] + SCALE, 'y': node_coords['y'] + SCALE}
            right_neighbour_coords = {'x': node_coords['x'] + SCALE, 'y': node_coords['y']}
            down_right_neighbour_coords = {'x': node_coords['x'] + SCALE, 'y': node_coords['y'] - SCALE}
            down_neighbour_coords = {'x': node_coords['x'], 'y': node_coords['y'] - SCALE}
            down_left_neighbour_coords = {'x': node_coords['x'] - SCALE, 'y': node_coords['y'] - SCALE}

            if ((self.check_exist_node(left_neighbour_coords) and
                 self.check_exist_node(upper_neighbour_coords)) and
                    (not self.check_exist_node(upper_left_neighbour_coords))):
                self.nodes_connections[
                    self.get_name_by_coords(left_neighbour_coords) + '->' + self.get_name_by_coords(upper_neighbour_coords)] = [
                    [left_neighbour_coords, upper_left_neighbour_coords, upper_neighbour_coords]]

            if ((self.check_exist_node(upper_neighbour_coords) and
                 self.check_exist_node(right_neighbour_coords)) and
                    (not self.check_exist_node(upper_right_neighbour_coords))):
                self.nodes_connections[
                    self.get_name_by_coords(upper_neighbour_coords) + '->' + self.get_name_by_coords(right_neighbour_coords)] = [
                    [upper_neighbour_coords, upper_right_neighbour_coords, right_neighbour_coords]]

            if ((self.check_exist_node(right_neighbour_coords) and
                 self.check_exist_node(down_neighbour_coords)) and
                    (not self.check_exist_node(down_right_neighbour_coords))):
                self.nodes_connections[
                    self.get_name_by_coords(right_neighbour_coords) + '->' + self.get_name_by_coords(down_neighbour_coords)] = [
                    [right_neighbour_coords, down_right_neighbour_coords, down_neighbour_coords]]

            if ((self.check_exist_node(down_neighbour_coords) and
                 self.check_exist_node(left_neighbour_coords)) and
                    (not self.check_exist_node(down_left_neighbour_coords))):
                self.nodes_connections[
                    self.get_name_by_coords(down_neighbour_coords) + '->' + self.get_name_by_coords(left_neighbour_coords)] = [
                    [down_neighbour_coords, down_left_neighbour_coords, left_neighbour_coords]]

        backup = copy.deepcopy(self.nodes_connections)

        while True:
            revert_flag = False
            self.nodes_connections = copy.deepcopy(backup)

            while self.get_num_branches() < self.branches_num:

                if revert_flag:
                    self.nodes_connections = copy.deepcopy(backup)
                    revert_flag = False

                locked_nodes = self.find_blocked_nodes()
                available_nodes = []
                for node_name, node_coords in self.nodes.items():
                    if {node_name: node_coords} not in locked_nodes:
                        available_nodes.append(node_coords)

                if len(available_nodes) < 2:
                    revert_flag = True
                else:
                    num_unavailable_node_pairs = 0
                    for node1, node2 in combinations(available_nodes, 2):
                        node1_name = self.get_name_by_coords(node1)
                        node2_name = self.get_name_by_coords(node2)

                        if self.get_num_connections_between_nodes(node1_name, node2_name) > 2:
                            num_unavailable_node_pairs += 1

                    if num_unavailable_node_pairs == len(available_nodes) * (len(available_nodes) - 1) // 2:
                        revert_flag = True

                if not revert_flag:
                    while True:
                        two_free_nodes = get_random_elements(available_nodes, 2)
                        node1_name = self.get_name_by_coords(two_free_nodes[0])
                        node2_name = self.get_name_by_coords(two_free_nodes[1])

                        if self.get_num_connections_between_nodes(node1_name, node2_name) <= 2:
                            break

                    self.connect_two_nodes(two_free_nodes[0], two_free_nodes[1])

            if all(self.count_node_connections(node) >= 3 for node in self.nodes.keys()):
                break
            else:
                continue

    def get_num_connections_between_nodes(self, node1_name, node2_name):
        num_connections = 0

        for connected_nodes, connection_coords in self.nodes_connections.items():
            if (connected_nodes == (node1_name + '->' + node2_name)) or (
                    connected_nodes == (node2_name + '->' + node1_name)):
                num_connections += len(connection_coords)

        return num_connections

    def count_node_connections(self, node_name):
        count = 0
        for connection, paths in self.nodes_connections.items():
            node1, node2 = connection.split('->')

            if node_name == node1 or node_name == node2:
                count += len(paths)

        return count

    def visualise_circuit(self):
        plt.figure(figsize=(5, 5))
        plt.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray')
        plt.xticks(range(-13, 14, 1))
        plt.yticks(range(-13, 14, 1))
        plt.xlim(-13, 13)
        plt.ylim(-13, 13)
        plt.axis('equal')

        for node, coords in self.nodes.items():
            plt.plot(coords['x'], coords['y'], 'ko')

        for key, value in self.nodes_connections.items():
            for connection in value:
                for i in range(0, len(connection)):
                    if i + 1 < len(connection):
                        plt.plot([connection[i]['x'], connection[i + 1]['x']],
                                 [connection[i]['y'], connection[i + 1]['y']], 'k-')

        plt.show()

    def find_bounds(self):
        min_x = float('inf')
        max_x = float('-inf')
        min_y = float('inf')
        max_y = float('-inf')

        for path in self.nodes_connections.values():
            for segment in path:
                for point in segment:
                    x = point['x']
                    y = point['y']

                    if x < min_x:
                        min_x = x
                    if x > max_x:
                        max_x = x
                    if y < min_y:
                        min_y = y
                    if y > max_y:
                        max_y = y

        return {
            'left': min_x,
            'right': max_x,
            'bottom': min_y,
            'top': max_y
        }

    def check_node_type(self, checking_node_coords):
        node_type = None

        min_x = float('inf')
        max_x = float('-inf')
        min_y = float('inf')
        max_y = float('-inf')

        for node, coords in self.nodes.items():
            if coords['x'] > max_x:
                max_x = coords['x']
            if coords['x'] < min_x:
                min_x = coords['x']
            if coords['y'] > max_y:
                max_y = coords['y']
            if coords['y'] < min_y:
                min_y = coords['y']

        if checking_node_coords['x'] == max_x:
            if checking_node_coords['y'] == max_y:
                node_type = 'upper_right'
            elif checking_node_coords['y'] == min_y:
                node_type = 'bottom_right'

        elif checking_node_coords['x'] == min_x:
            if checking_node_coords['y'] == max_y:
                node_type = 'upper_left'
            elif checking_node_coords['y'] == min_y:
                node_type = 'bottom_left'

        elif checking_node_coords['y'] == max_y:
            node_type = 'upper_middle'

        elif checking_node_coords['y'] == min_y:
            node_type = 'bottom_middle'

        return node_type

    def connect_two_nodes(self, node1, node2):
        bounds = self.find_bounds()
        node1_type = self.check_node_type(node1)
        node2_type = self.check_node_type(node2)

        if (node1_type == 'bottom_middle') or (node2_type == 'bottom_middle'):
            bottom_node = node1
            not_bottom_node = node2

            if node2_type == 'bottom_middle':
                bottom_node = node2
                not_bottom_node = node1

            # *-------|
            # |       |
            # |       |
            # |---*---|
            if self.check_node_type(not_bottom_node) == 'upper_left':
                connections = [
                    bottom_node,
                    {'x': bottom_node['x'], 'y': bounds['bottom'] - SCALE / 2},
                    {'x': bounds['left'] - SCALE / 2, 'y': bounds['bottom'] - SCALE / 2},
                    {'x': bounds['left'] - SCALE / 2, 'y': not_bottom_node['y']},
                    not_bottom_node
                ]
                if (self.get_name_by_coords(node1) + '->' + self.get_name_by_coords(node2)) in self.nodes_connections:
                    self.nodes_connections[self.get_name_by_coords(node1) + '->' + self.get_name_by_coords(node2)].append(
                        connections
                    )
                else:
                    self.nodes_connections[self.get_name_by_coords(node1) + '->' + self.get_name_by_coords(node2)] = [
                        connections
                    ]

            # |-------*
            # |       |
            # |       |
            # |---*---|
            if self.check_node_type(not_bottom_node) == 'upper_right':
                connections = [
                    bottom_node,
                    {'x': bottom_node['x'], 'y': bounds['bottom'] - SCALE / 2},
                    {'x': bounds['right'] + SCALE / 2, 'y': bounds['bottom'] - SCALE / 2},
                    {'x': bounds['right'] + SCALE / 2, 'y': not_bottom_node['y']},
                    not_bottom_node
                ]
                if (self.get_name_by_coords(node1) + '->' + self.get_name_by_coords(node2)) in self.nodes_connections:
                    self.nodes_connections[self.get_name_by_coords(node1) + '->' + self.get_name_by_coords(node2)].append(
                        connections
                    )
                else:
                    self.nodes_connections[self.get_name_by_coords(node1) + '->' + self.get_name_by_coords(node2)] = [
                        connections
                    ]
        else:
            nodes_connections_key = self.get_name_by_coords(node1) + '->' + self.get_name_by_coords(node2)
            if node1['x'] == node2['x']:

                # *-------|
                # |       |
                # |       |
                # *-------|
                if (node1_type == 'upper_left') or (node1_type == 'bottom_left'):
                    connections = [
                        node1,
                        {'x': bounds['left'] - SCALE / 2, 'y': node1['y']},
                        {'x': bounds['left'] - SCALE / 2, 'y': node2['y']},
                        node2
                    ]
                    if nodes_connections_key in self.nodes_connections:
                        self.nodes_connections[nodes_connections_key].append(
                            connections
                        )
                    else:
                        self.nodes_connections[nodes_connections_key] = [
                            connections
                        ]

                # |-------*
                # |       |
                # |       |
                # |-------*
                elif (node1_type == 'upper_right') or (node1_type == 'bottom_right'):
                    connections = [
                        node1,
                        {'x': bounds['right'] + SCALE / 2, 'y': node1['y']},
                        {'x': bounds['right'] + SCALE / 2, 'y': node2['y']},
                        node2
                    ]
                    if nodes_connections_key in self.nodes_connections:
                        self.nodes_connections[nodes_connections_key].append(
                            connections
                        )
                    else:
                        self.nodes_connections[nodes_connections_key] = [
                            connections
                        ]

            elif node1['y'] == node2['y']:

                # *-------*
                if self.nodes_num == 2:
                    connections = [
                        [
                            node1,
                            {'x': node1['x'], 'y': node1['y'] + SCALE / 2},
                            {'x': node2['x'], 'y': node2['y'] + SCALE / 2},
                            node2
                        ],
                        [
                            node1,
                            {'x': node1['x'], 'y': node1['y'] - SCALE / 2},
                            {'x': node2['x'], 'y': node2['y'] - SCALE / 2},
                            node2
                        ]
                    ]
                    if nodes_connections_key in self.nodes_connections:
                        self.nodes_connections[nodes_connections_key].extend(
                            connections
                        )
                    else:
                        self.nodes_connections[nodes_connections_key] = connections

                # *-------*
                # |       |
                # |       |
                # |-------|
                elif (node1_type == 'upper_left') or (node1_type == 'upper_right'):
                    connections = [
                        node1,
                        {'x': node1['x'], 'y': bounds['top'] + SCALE/2},
                        {'x': node2['x'], 'y': bounds['top'] + SCALE/2},
                        node2
                    ]
                    if nodes_connections_key in self.nodes_connections:
                        self.nodes_connections[nodes_connections_key].append(
                            connections
                        )
                    else:
                        self.nodes_connections[nodes_connections_key] = [
                            connections
                        ]

                # |-------|
                # |       |
                # |       |
                # *-------*
                elif (node1_type == 'bottom_right') or (node1_type == 'bottom_left'):
                    connections = [
                        node1,
                        {'x': node1['x'], 'y': bounds['bottom'] - SCALE/2},
                        {'x': node2['x'], 'y': bounds['bottom'] - SCALE/2},
                        node2
                    ]
                    if nodes_connections_key in self.nodes_connections:
                        self.nodes_connections[nodes_connections_key].append(
                            connections
                        )
                    else:
                        self.nodes_connections[nodes_connections_key] = [
                            connections
                        ]

            #    |-------*(1)
            #    |       |
            #    |       |
            # (2)*-------|
            elif (node1['x'] > node2['x']) and (node1['y'] > node2['y']):
                connections = [
                    [
                        node1,
                        {'x': node1['x'], 'y': bounds['top'] + SCALE / 2},
                        {'x': bounds['left'] - SCALE / 2, 'y': bounds['top'] + SCALE / 2},
                        {'x': bounds['left'] - SCALE / 2, 'y': node2['y']},
                        node2
                    ],
                    [
                        node1,
                        {'x': bounds['right'] + SCALE / 2, 'y': node1['y']},
                        {'x': bounds['right'] + SCALE / 2, 'y': bounds['bottom'] - SCALE / 2},
                        {'x': node2['x'], 'y': bounds['bottom'] - SCALE / 2},
                        node2
                    ]
                ]
                if nodes_connections_key in self.nodes_connections:
                    self.nodes_connections[nodes_connections_key].append(
                        get_random_elements(connections, 1)[0]
                    )
                else:
                    self.nodes_connections[nodes_connections_key] = [
                        get_random_elements(connections, 1)[0]
                    ]

            # (2)*-------|
            #    |       |
            #    |       |
            #    |-------*(1)
            elif (node1['x'] > node2['x']) and (node1['y'] < node2['y']):
                connections = [
                    [
                        node1,
                        {'x': node1['x'], 'y': bounds['bottom'] - SCALE / 2},
                        {'x': bounds['left'] - SCALE / 2, 'y': bounds['bottom'] - SCALE / 2},
                        {'x': bounds['left'] - SCALE / 2, 'y': node2['y']},
                        node2
                    ],
                    [
                        node1,
                        {'x': bounds['right'] + SCALE / 2, 'y': node1['y']},
                        {'x': bounds['right'] + SCALE / 2, 'y': bounds['top'] + SCALE / 2},
                        {'x': node2['x'], 'y': bounds['top'] + SCALE / 2},
                        node2
                    ]
                ]
                if nodes_connections_key in self.nodes_connections:
                    self.nodes_connections[nodes_connections_key].append(
                        get_random_elements(connections, 1)[0]
                    )
                else:
                    self.nodes_connections[nodes_connections_key] = [
                        get_random_elements(connections, 1)[0]
                    ]

            #    |-------*(2)
            #    |       |
            #    |       |
            # (1)*-------|
            elif (node1['x'] < node2['x']) and (node1['y'] < node2['y']):
                connections = [
                    [
                        node1,
                        {'x': bounds['left'] - SCALE / 2, 'y': node1['y']},
                        {'x': bounds['left'] - SCALE / 2, 'y': bounds['top'] + SCALE / 2},
                        {'x': node2['x'], 'y': bounds['top'] + SCALE / 2},
                        node2
                    ],
                    [
                        node1,
                        {'x': node1['x'], 'y': bounds['bottom'] - SCALE / 2},
                        {'x': bounds['right'] + SCALE / 2, 'y': bounds['bottom'] - SCALE / 2},
                        {'x': bounds['right'] + SCALE / 2, 'y': node2['y']},
                        node2
                    ]
                ]
                if nodes_connections_key in self.nodes_connections:
                    self.nodes_connections[nodes_connections_key].append(
                        get_random_elements(connections, 1)[0]
                    )
                else:
                    self.nodes_connections[nodes_connections_key] = [
                        get_random_elements(connections, 1)[0]
                    ]

            # (1)*-------|
            #    |       |
            #    |       |
            #    |-------*(2)
            elif (node1['x'] < node2['x']) and (node1['y'] > node2['y']):
                connections = [
                    [
                        node1,
                        {'x': node1['x'], 'y': bounds['top'] + SCALE / 2},
                        {'x': bounds['right'] + SCALE / 2, 'y': bounds['top'] + SCALE / 2},
                        {'x': bounds['right'] + SCALE / 2, 'y': node2['y']},
                        node2
                    ],
                    [
                        node1,
                        {'x': bounds['left'] - SCALE / 2, 'y': node1['y']},
                        {'x': bounds['left'] - SCALE / 2, 'y': bounds['bottom'] - SCALE / 2},
                        {'x': node2['x'], 'y': bounds['bottom'] - SCALE / 2},
                        node2
                    ]
                ]
                if nodes_connections_key in self.nodes_connections:
                    self.nodes_connections[nodes_connections_key].append(
                        get_random_elements(connections, 1)[0]
                    )
                else:
                    self.nodes_connections[nodes_connections_key] = [
                        get_random_elements(connections, 1)[0]
                    ]

    def find_blocked_nodes(self):
        def find_intersection(line1, line2):
            A, B = line1
            C, D = line2

            if A['y'] == B['y'] and C['x'] == D['x']:
                if (min(C['y'], D['y']) <= A['y'] <= max(C['y'], D['y']) and
                        min(A['x'], B['x']) <= C['x'] <= max(A['x'], B['x'])):
                    return {'x': C['x'], 'y': A['y']}

            if A['x'] == B['x'] and C['y'] == D['y']:
                if (min(A['y'], B['y']) <= C['y'] <= max(A['y'], B['y']) and
                        min(C['x'], D['x']) <= A['x'] <= max(C['x'], D['x'])):
                    return {'x': A['x'], 'y': C['y']}

            return None

        contour_lines = []
        locked_nodes = []

        for key, value in self.nodes_connections.items():
            for connection in value:
                for i in range(0, len(connection)):
                    if i + 1 < len(connection):
                        contour_lines.append(
                            [
                                {'x': connection[i]['x'], 'y': connection[i]['y']},
                                {'x': connection[i + 1]['x'], 'y': connection[i + 1]['y']}
                            ]
                        )

        contour_lines_tails = []
        for contour_line in contour_lines:
            contour_lines_tails.append(contour_line[0])

        for node, coords in self.nodes.items():

            node_type = self.check_node_type(coords)

            if node_type == 'upper_left':
                node_lines = [
                    [{'x': coords['x'], 'y': coords['y']}, {'x': coords['x'], 'y': 100 * SCALE}],
                    [{'x': coords['x'], 'y': coords['y']}, {'x': -100 * SCALE, 'y': coords['y']}]
                ]

            elif node_type == 'bottom_left':
                node_lines = [
                    [{'x': coords['x'], 'y': coords['y']}, {'x': coords['x'], 'y': -100 * SCALE}],
                    [{'x': coords['x'], 'y': coords['y']}, {'x': -100 * SCALE, 'y': coords['y']}]
                ]

            elif node_type == 'upper_right':
                node_lines = [
                    [{'x': coords['x'], 'y': coords['y']}, {'x': coords['x'], 'y': 100 * SCALE}],
                    [{'x': coords['x'], 'y': coords['y']}, {'x': 100 * SCALE, 'y': coords['y']}],
                ]

            elif node_type == 'bottom_right':
                node_lines = [
                    [{'x': coords['x'], 'y': coords['y']}, {'x': coords['x'], 'y': -100 * SCALE}],
                    [{'x': coords['x'], 'y': coords['y']}, {'x': 100 * SCALE, 'y': coords['y']}],
                ]

            elif node_type == 'upper_middle':
                node_lines = [
                    [{'x': coords['x'], 'y': coords['y']}, {'x': coords['x'], 'y': 100 * SCALE}]
                ]

            elif node_type == 'bottom_middle':
                node_lines = [
                    [{'x': coords['x'], 'y': coords['y']}, {'x': coords['x'], 'y': -100 * SCALE}],
                ]

            for node_line in node_lines:
                for contour_line in contour_lines:
                    intersection_dot = find_intersection(node_line, contour_line)
                    if intersection_dot:
                        contour_line_tails = [contour_line[0], contour_line[1]]
                        if not (intersection_dot in contour_line_tails):
                            if node not in locked_nodes:
                                locked_nodes.append({node: coords})

        return locked_nodes

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
