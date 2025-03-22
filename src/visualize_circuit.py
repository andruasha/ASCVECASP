import matplotlib.pyplot as plt


class CircuitVisualize:

    def __init__(self, circuit, circuit_topology):
        self.circuit = circuit
        self.circuit_topology = circuit_topology

    def visualize(self):
        plt.figure(figsize=(5, 5))
        plt.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray')
        plt.xticks(range(-13, 14, 1))
        plt.yticks(range(-13, 14, 1))
        plt.xlim(-13, 13)
        plt.ylim(-13, 13)
        plt.axis('equal')

        for node, coords in self.circuit_topology.nodes.items():
            plt.plot(coords['x'], coords['y'], 'ko')

        for connections in self.circuit.layout.values():
            for segment in connections:
                segment_connections = segment[0]['connection_coords']
                for i in range(len(segment_connections) - 1):
                    start, end = segment_connections[i], segment_connections[i + 1]
                    plt.plot([start['x'], end['x']], [start['y'], end['y']], 'k-')

                segment_elements = segment[0]['elements']
                if segment_elements:
                    free_lines = self.get_free_lines(segment_connections)

                    num_elements = len(segment_elements)
                    num_lines = len(free_lines)

                    if num_lines == 0:
                        continue

                    for idx, element in enumerate(segment_elements):
                        line_idx = idx % num_lines
                        line = free_lines[line_idx]
                        start, end = line

                        if num_lines == 1:
                            t = (idx + 1) / (num_elements + 1)
                            x = start['x'] + t * (end['x'] - start['x'])
                            y = start['y'] + t * (end['y'] - start['y'])
                        else:
                            x = (start['x'] + end['x']) / 2
                            y = (start['y'] + end['y']) / 2

                        offset = 0.3
                        plt.text(x, y + offset, self.get_element_symbol(element['type']),
                                 fontsize=10, ha='center', va='center', color='blue')

        plt.show()

    def get_free_lines(self, target_segment):
        def is_point_on_segment(p, a, b, tol=1e-9):
            cross = (b['x'] - a['x']) * (p['y'] - a['y']) - (b['y'] - a['y']) * (p['x'] - a['x'])
            if abs(cross) > tol:
                return False
            dot = (p['x'] - a['x']) * (b['x'] - a['x']) + (p['y'] - a['y']) * (b['y'] - a['y'])
            if dot < 0:
                return False
            squared_length_ab = (b['x'] - a['x']) ** 2 + (b['y'] - a['y']) ** 2
            return dot <= squared_length_ab

        def is_line_nested(inner_line, outer_line):
            a1, b1 = inner_line
            a2, b2 = outer_line
            return (
                    (a1 == a2 and is_point_on_segment(b1, a2, b2)) or
                    (a1 == b2 and is_point_on_segment(b1, b2, a2)) or
                    (b1 == a2 and is_point_on_segment(a1, a2, b2)) or
                    (b1 == b2 and is_point_on_segment(a1, b2, a2))
            )

        all_lines = []
        for connections in self.circuit.layout.values():
            for segment in connections:
                segment_connections = segment[0]['connection_coords']
                if segment_connections != target_segment:
                    for i in range(len(segment_connections) - 1):
                        start, end = segment_connections[i], segment_connections[i + 1]
                        all_lines.append([start, end])

        segment_lines = []
        for i in range(len(target_segment) - 1):
            start, end = target_segment[i], target_segment[i + 1]
            segment_lines.append([start, end])

        excluded_lines = set()

        for seg_line in segment_lines:
            for other_line in all_lines:
                if is_line_nested(seg_line, other_line) or is_line_nested(other_line, seg_line):
                    excluded_lines.add(
                        tuple(map(tuple, [(seg_line[0]['x'], seg_line[0]['y']), (seg_line[1]['x'], seg_line[1]['y'])])))
                    break

        free_lines = []
        for line in segment_lines:
            line_key = tuple(map(tuple, [(line[0]['x'], line[0]['y']), (line[1]['x'], line[1]['y'])]))
            if line_key not in excluded_lines:
                free_lines.append(line)

        return free_lines

    def get_element_symbol(self, element_type):
        return {
            'resistor': 'R',
            'inductance': 'L',
            'capacity': 'C',
            'voltage_source': 'V',
            'current_source': 'I',
        }.get(element_type, '?')
