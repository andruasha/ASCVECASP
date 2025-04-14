from conf.config import SCALE

import matplotlib.pyplot as plt

from src.common.draw_functions import draw_resistor, draw_active_dipole, draw_current_source, draw_voltage_source


class CircuitVisualize:

    def __init__(self, circuit, circuit_topology):
        self.circuit = circuit
        self.circuit_topology = circuit_topology

    def export_to_ltspice(self, filename="circuit.cir"):
        lines = ["* Generated LTspice Netlist"]
        node_map = {}
        node_counter = 1

        def get_node_name(x, y):
            nonlocal node_counter
            key = (x, y)
            if key not in node_map:
                node_map[key] = f"N{node_counter:03}"
                node_counter += 1
            return node_map[key]

        resistor_idx = 1
        voltage_source_idx = 1
        current_source_idx = 1
        active_dipole_idx = 1

        for connections in self.circuit.layout.values():
            for segment in connections:
                segment_connections = segment[0]['connection_coords']
                segment_elements = segment[0]['elements']
                free_lines = self.get_free_lines(segment_connections)

                node_pairs = []
                for line in free_lines:
                    start = line[0]
                    end = line[1]
                    node_start = get_node_name(start['x'], start['y'])
                    node_end = get_node_name(end['x'], end['y'])
                    node_pairs.append((node_start, node_end))

                total_elements = len(segment_elements)
                num_lines = len(node_pairs)
                elements_per_line = total_elements // num_lines
                extra = total_elements % num_lines

                element_iter = iter(segment_elements)

                for line_idx, (n1, n2) in enumerate(node_pairs):
                    count = elements_per_line + (1 if line_idx < extra else 0)
                    for _ in range(count):
                        element = next(element_iter)
                        if element['type'] == 'resistor':
                            lines.append(f"R{resistor_idx} {n1} {n2} 1k")
                            resistor_idx += 1
                        elif element['type'] == 'voltage_source':
                            lines.append(f"V{voltage_source_idx} {n1} {n2} DC 5")
                            voltage_source_idx += 1
                        elif element['type'] == 'current_source':
                            lines.append(f"I{current_source_idx} {n1} {n2} DC 1m")
                            current_source_idx += 1
                        elif element['type'] == 'active_dipole':
                            lines.append(f"XAD{active_dipole_idx} {n1} {n2} active_dipole_model")
                            active_dipole_idx += 1

        lines.append(".end")

        with open(filename, "w") as f:
            f.write("\n".join(lines))

        print(f"LTspice netlist exported to: {filename}")

    def visualize(self):
        plt.figure(figsize=(5, 5))
        plt.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray')
        plt.xticks(range(-13, 14, 1))
        plt.yticks(range(-13, 14, 1))
        plt.xlim(-13, 13)
        plt.ylim(-13, 13)
        plt.axis('equal')

        for node, coords in self.circuit_topology.nodes.items():
            plt.plot(coords['x'], coords['y'], 'ko', markersize=3)

        resistor_idx = 1
        voltage_source_idx = 1
        current_source_idx = 1

        for connections in self.circuit.layout.values():
            for segment in connections:
                segment_connections = segment[0]['connection_coords']
                for i in range(len(segment_connections) - 1):
                    start, end = segment_connections[i], segment_connections[i + 1]
                    plt.plot([start['x'], end['x']], [start['y'], end['y']], 'k-', linewidth=1)

                segment_elements = segment[0]['elements']
                num_elements = len(segment_elements)
                free_lines = self.get_free_lines(segment_connections)
                num_lines = len(free_lines)

                if num_lines == 1:
                    start, end = free_lines[0]
                    if start['x'] == end['x']:
                        step = (abs(end['y'] - start['y']) / num_elements) / 2
                        current_position = min(end['y'], start['y']) + step
                        for element in segment_elements:
                            if element['type'] == 'resistor':
                                draw_resistor({'x': end['x'], 'y': current_position}, 'R' + str(resistor_idx),
                                              'vertical')
                                resistor_idx += 1
                            elif element['type'] == 'active_dipole':
                                draw_active_dipole({'x': end['x'], 'y': current_position}, 'vertical')
                            elif element['type'] == 'voltage_source':
                                draw_voltage_source({'x': end['x'], 'y': current_position},
                                                    'V' + str(voltage_source_idx), 'vertical')
                                voltage_source_idx += 1
                            elif element['type'] == 'current_source':
                                draw_current_source({'x': end['x'], 'y': current_position},
                                                    'I' + str(current_source_idx), 'vertical')
                                current_source_idx += 1
                            current_position += 2 * step
                    elif start['y'] == end['y']:
                        step = (abs(end['x'] - start['x']) / num_elements) / 2
                        current_position = min(end['x'], start['x']) + step
                        for element in segment_elements:
                            if element['type'] == 'resistor':
                                draw_resistor({'x': current_position, 'y': end['y']}, 'R' + str(resistor_idx),
                                              'horizontal')
                                resistor_idx += 1
                            elif element['type'] == 'active_dipole':
                                draw_active_dipole({'x': current_position, 'y': end['y']}, 'horizontal')
                            elif element['type'] == 'voltage_source':
                                draw_voltage_source({'x': current_position, 'y': end['y']},
                                                    'V' + str(voltage_source_idx), 'horizontal')
                                voltage_source_idx += 1
                            elif element['type'] == 'current_source':
                                draw_current_source({'x': current_position, 'y': end['y']},
                                                    'I' + str(current_source_idx), 'horizontal')
                                current_source_idx += 1
                            current_position += 2 * step

                elif num_lines > 1:
                    total_elements = len(segment_elements)
                    elements_per_line = total_elements // num_lines
                    extra = total_elements % num_lines

                    element_iter = iter(segment_elements)

                    for line_idx, (start, end) in enumerate(free_lines):
                        num_this_line = elements_per_line + (1 if line_idx < extra else 0)

                        if num_this_line == 0:
                            continue

                        if start['x'] == end['x']:
                            step = (abs(end['y'] - start['y']) / num_this_line) / 2
                            current_position = min(end['y'], start['y']) + step
                            for _ in range(num_this_line):
                                element = next(element_iter)
                                pos = {'x': end['x'], 'y': current_position}
                                if element['type'] == 'resistor':
                                    draw_resistor(pos, 'R' + str(resistor_idx), 'vertical')
                                    resistor_idx += 1
                                elif element['type'] == 'active_dipole':
                                    draw_active_dipole(pos, 'vertical')
                                elif element['type'] == 'voltage_source':
                                    draw_voltage_source(pos, 'V' + str(voltage_source_idx), 'vertical')
                                    voltage_source_idx += 1
                                elif element['type'] == 'current_source':
                                    draw_current_source(pos, 'I' + str(current_source_idx), 'vertical')
                                    current_source_idx += 1
                                current_position += 2 * step

                        elif start['y'] == end['y']:
                            step = (abs(end['x'] - start['x']) / num_this_line) / 2
                            current_position = min(end['x'], start['x']) + step
                            for _ in range(num_this_line):
                                element = next(element_iter)
                                pos = {'x': current_position, 'y': end['y']}
                                if element['type'] == 'resistor':
                                    draw_resistor(pos, 'R' + str(resistor_idx), 'horizontal')
                                    resistor_idx += 1
                                elif element['type'] == 'active_dipole':
                                    draw_active_dipole(pos, 'horizontal')
                                elif element['type'] == 'voltage_source':
                                    draw_voltage_source(pos, 'V' + str(voltage_source_idx), 'horizontal')
                                    voltage_source_idx += 1
                                elif element['type'] == 'current_source':
                                    draw_current_source(pos, 'I' + str(current_source_idx), 'horizontal')
                                    current_source_idx += 1
                                current_position += 2 * step

        plt.axis('off')
        return plt

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
