import matplotlib.pyplot as plt
import random

scale = 5


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
                                'node2': {'x': scale, 'y': 0}}

        template_two_nodes_2 = {'node1': {'x': 0, 'y': 0},
                                'node2': {'x': 0, 'y': scale}}

        template_three_nodes_1 = {'node1': {'x': 0, 'y': 0},
                                  'node2': {'x': 0, 'y': scale},
                                  'node3': {'x': scale, 'y': scale}}

        template_three_nodes_2 = {'node1': {'x': 0, 'y': scale},
                                  'node2': {'x': scale, 'y': scale},
                                  'node3': {'x': scale, 'y': 0}}

        template_three_nodes_3 = {'node1': {'x': scale, 'y': scale},
                                  'node2': {'x': scale, 'y': 0},
                                  'node3': {'x': 0, 'y': 0}}

        template_four_nodes_1 = {'node1': {'x': 0, 'y': 0},
                                 'node2': {'x': 0, 'y': scale},
                                 'node3': {'x': scale, 'y': scale},
                                 'node4': {'x': scale, 'y': 0}}

        template_four_nodes_2 = {'node1': {'x': 0, 'y': scale},
                                 'node2': {'x': scale, 'y': scale},
                                 'node3': {'x': 2 * scale, 'y': scale},
                                 'node4': {'x': scale, 'y': 0}}

        template_four_nodes_3 = {'node1': {'x': 0, 'y': scale},
                                 'node2': {'x': scale, 'y': 2 * scale},
                                 'node3': {'x': scale, 'y': scale},
                                 'node4': {'x': scale, 'y': 0}}

        template_four_nodes_4 = {'node1': {'x': scale, 'y': scale},
                                 'node2': {'x': 2 * scale, 'y': 0},
                                 'node3': {'x': scale, 'y': 0},
                                 'node4': {'x': 0, 'y': 0}}

        template_four_nodes_5 = {'node1': {'x': 0, 'y': 0},
                                 'node2': {'x': 0, 'y': scale},
                                 'node3': {'x': 0, 'y': 2 * scale},
                                 'node4': {'x': scale, 'y': scale}}

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

        single_nodes = self.get_single_nodes()
        third_node_coords = {}

        if len(single_nodes) == 2:
            for node, coords in self.nodes_coords.items():
                if node not in single_nodes.keys():
                    third_node_coords = coords
            keys = list(single_nodes.keys())
            values = list(single_nodes.values())
            imaginary_node_coords = {'x': values[0]['x'] + values[1]['x'] - third_node_coords['x'],
                                     'y': values[0]['y'] + values[1]['y'] - third_node_coords['y']}
            self.nodes_connections[keys[0] + '->' + keys[1]] = [[values[0], imaginary_node_coords, values[1]]]

        if len(single_nodes) == 1:
            single_node_coords = self.get_node_coords(single_nodes)
            single_node_name = self.get_node_name(single_nodes)
            near_node = self.get_near_nodes(single_nodes)
            near_node_name = self.get_node_name(near_node[0])
            near_node_coords = self.get_node_coords(near_node[0])

            upper_near_of_near_node_coords = None
            lower_near_of_near_node_coords = None
            right_near_of_near_node_coords = None
            left_near_of_near_node_coords = None

            if self.check_exist_node({'x': near_node_coords['x'], 'y': near_node_coords['y'] + 5}):
                upper_near_of_near_node_coords = {'x': near_node_coords['x'], 'y': near_node_coords['y'] + 5}
            if self.check_exist_node({'x': near_node_coords['x'], 'y': near_node_coords['y'] - 5}):
                lower_near_of_near_node_coords = {'x': near_node_coords['x'], 'y': near_node_coords['y'] - 5}
            if self.check_exist_node({'x': near_node_coords['x'] + 5, 'y': near_node_coords['y']}):
                right_near_of_near_node_coords = {'x': near_node_coords['x'] + 5, 'y': near_node_coords['y']}
            if self.check_exist_node({'x': near_node_coords['x'] - 5, 'y': near_node_coords['y']}):
                left_near_of_near_node_coords = {'x': near_node_coords['x'] - 5, 'y': near_node_coords['y']}

            if (near_node_coords['y'] > single_node_coords['y']) or (near_node_coords['y'] < single_node_coords['y']):
                if left_near_of_near_node_coords and right_near_of_near_node_coords:
                    nn_coords = random.choice([left_near_of_near_node_coords, right_near_of_near_node_coords])
                elif left_near_of_near_node_coords:
                    nn_coords = left_near_of_near_node_coords
                else:
                    nn_coords = right_near_of_near_node_coords

                imaginary_node_coords = {'x': single_node_coords['x'] + nn_coords['x'] - near_node_coords['x'],
                                         'y': single_node_coords['y'] + nn_coords['y'] - near_node_coords['y']}
                self.nodes_connections[single_node_name + '->' + near_node_name] = [[single_node_coords,
                                                                                     imaginary_node_coords,
                                                                                     nn_coords]]
            else:
                if upper_near_of_near_node_coords and lower_near_of_near_node_coords:
                    nn_coords = random.choice([upper_near_of_near_node_coords, lower_near_of_near_node_coords])
                elif upper_near_of_near_node_coords:
                    nn_coords = upper_near_of_near_node_coords
                else:
                    nn_coords = lower_near_of_near_node_coords

                imaginary_node_coords = {'x': single_node_coords['x'] + nn_coords['x'] - near_node_coords['x'],
                                         'y': single_node_coords['y'] + nn_coords['y'] - near_node_coords['y']}
                self.nodes_connections[single_node_name + '->' + near_node_name] = [[single_node_coords,
                                                                                     imaginary_node_coords,
                                                                                     nn_coords]]

    def get_near_nodes(self, target_node):
        target_node_coords = self.get_node_coords(target_node)
        near_nodes = []
        for node, coords in self.nodes_coords.items():
            if (coords == {'x': target_node_coords['x'] + 5, 'y': target_node_coords['y']} or
                    coords == {'x': target_node_coords['x'] - 5, 'y': target_node_coords['y']} or
                    coords == {'x': target_node_coords['x'], 'y': target_node_coords['y'] + 5} or
                    coords == {'x': target_node_coords['x'], 'y': target_node_coords['y'] - 5}):
                near_nodes.append({node: coords})
        return near_nodes

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

    def get_contour(self):
        def check_exist_line(lines, target_line):
            for i in lines:
                if target_line == i:
                    return True
            return False

        lines = []
        contour_lines = []
        contour_points = []

        for key, value in self.nodes_connections.items():
            for connection in value:
                for i in range(0, len(connection)):
                    if i + 1 < len(connection):
                        line = [{'x': connection[i]['x'], 'y': connection[i]['y']},
                                {'x': connection[i + 1]['x'], 'y': connection[i + 1]['y']}]
                        lines.append(line)

        for line in lines:
            if line[0]['x'] == line[1]['x']:
                target_neighbour_1 = [{'x': line[0]['x'] + 5, 'y': line[0]['y']},
                                      {'x': line[1]['x'] + 5, 'y': line[1]['y']}]
                target_neighbour_2 = [{'x': line[1]['x'] + 5, 'y': line[1]['y']},
                                      {'x': line[0]['x'] + 5, 'y': line[0]['y']}]
                target_neighbour_3 = [{'x': line[0]['x'] - 5, 'y': line[0]['y']},
                                      {'x': line[1]['x'] - 5, 'y': line[1]['y']}]
                target_neighbour_4 = [{'x': line[1]['x'] - 5, 'y': line[1]['y']},
                                      {'x': line[0]['x'] - 5, 'y': line[0]['y']}]

                if (
                        (
                                (check_exist_line(lines, target_neighbour_1) is False) and
                                (check_exist_line(lines, target_neighbour_2) is False)
                        ) or
                        (
                                (check_exist_line(lines, target_neighbour_3) is False) and
                                (check_exist_line(lines, target_neighbour_4) is False)
                        )
                ):
                    contour_lines.append(line)

            elif line[0]['y'] == line[1]['y']:
                target_neighbour_1 = [{'x': line[0]['x'], 'y': line[0]['y'] + 5},
                                      {'x': line[1]['x'], 'y': line[1]['y'] + 5}]
                target_neighbour_2 = [{'x': line[1]['x'], 'y': line[1]['y'] + 5},
                                      {'x': line[0]['x'], 'y': line[0]['y'] + 5}]
                target_neighbour_3 = [{'x': line[0]['x'], 'y': line[0]['y'] - 5},
                                      {'x': line[1]['x'], 'y': line[1]['y'] - 5}]
                target_neighbour_4 = [{'x': line[1]['x'], 'y': line[1]['y'] - 5},
                                      {'x': line[0]['x'], 'y': line[0]['y'] - 5}]

                if (
                        (
                                (check_exist_line(lines, target_neighbour_1) is False) and
                                (check_exist_line(lines, target_neighbour_2) is False)
                        ) or
                        (
                                (check_exist_line(lines, target_neighbour_3) is False) and
                                (check_exist_line(lines, target_neighbour_4) is False)
                        )
                ):
                    contour_lines.append(line)

        for line in contour_lines:
            for i in range(0, 2):
                if {'x': line[i]['x'], 'y': line[i]['y']} not in contour_points:
                    contour_points.append({'x': line[i]['x'], 'y': line[i]['y']})

        return contour_lines

    @staticmethod
    def get_node_name(target_node):
        return list(target_node.keys())[0]

    @staticmethod
    def get_node_coords(target_node):
        return list(target_node.values())[0]
