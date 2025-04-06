from conf.config import SCALE

import matplotlib.pyplot as plt
import secrets
import numpy as np


def get_random_elements(elements_array, elements_num):
    return secrets.SystemRandom().sample(elements_array, elements_num)


def draw_resistor(center, name, orientation):
    width = SCALE / 10
    height = SCALE / 20

    if orientation == 'horizontal':
        lower_left = (center['x'] - width / 2, center['y'] - height / 2)
        rect_width, rect_height = width, height
        text_x, text_y = center['x'], center['y'] - height * 1.2
        ha, va = 'center', 'top'
    if orientation == 'vertical':
        lower_left = (center['x'] - height / 2, center['y'] - width / 2)
        rect_width, rect_height = height, width
        text_x, text_y = center['x'] + height * 1.2, center['y']
        ha, va = 'left', 'center'

    rect = plt.Rectangle(
        lower_left,
        rect_width, rect_height,
        linewidth=1.0,
        edgecolor='black',
        facecolor='white',
        zorder=10
    )

    plt.gca().add_patch(rect)
    plt.text(text_x, text_y, name, fontsize=6, ha=ha, va=va, color='blue', zorder=11)


def draw_capacitor(center, name, orientation):
    plate_length = SCALE / 20
    gap = SCALE / 40
    cover_thickness = SCALE / 80

    if orientation == 'horizontal':
        x1 = center['x'] - gap / 2
        x2 = center['x'] + gap / 2
        y_top = center['y'] + plate_length / 2
        y_bottom = center['y'] - plate_length / 2

        plt.plot([x1, x1], [y_bottom, y_top], color='black', linewidth=1.0, zorder=10)
        plt.plot([x2, x2], [y_bottom, y_top], color='black', linewidth=1.0, zorder=10)

        rect = plt.Rectangle(
            (x1, y_bottom),
            x2 - x1, y_top - y_bottom,
            facecolor='white',
            edgecolor='none',
            zorder=9.5
        )
        plt.gca().add_patch(rect)

        text_x, text_y = center['x'], center['y'] - plate_length
        ha, va = 'center', 'top'

    elif orientation == 'vertical':
        y1 = center['y'] - gap / 2
        y2 = center['y'] + gap / 2
        x_left = center['x'] - plate_length / 2
        x_right = center['x'] + plate_length / 2

        plt.plot([x_left, x_right], [y1, y1], color='black', linewidth=1.0, zorder=10)
        plt.plot([x_left, x_right], [y2, y2], color='black', linewidth=1.0, zorder=10)

        rect = plt.Rectangle(
            (x_left, y1),
            x_right - x_left, y2 - y1,
            facecolor='white',
            edgecolor='none',
            zorder=9.5
        )
        plt.gca().add_patch(rect)

        text_x, text_y = center['x'] + plate_length, center['y']
        ha, va = 'left', 'center'

    plt.text(text_x, text_y, name, fontsize=6, ha=ha, va=va, color='blue', zorder=11)


def draw_inductor(center, name, orientation):
    num_loops = 3
    loop_radius = SCALE / 40
    loop_spacing = loop_radius * 2
    total_length = loop_spacing * num_loops
    height = SCALE / 20

    if orientation == 'horizontal':
        start_x = center['x'] - total_length / 2
        y_center = center['y']

        rect = plt.Rectangle(
            (start_x, y_center - loop_radius),
            total_length, loop_radius * 2,
            facecolor='white',
            edgecolor='none',
            zorder=9.5
        )
        plt.gca().add_patch(rect)

        for i in range(num_loops):
            theta = np.linspace(0, np.pi, 100)
            x = start_x + i * loop_spacing + loop_radius * (1 - np.cos(theta))
            y = y_center + loop_radius * np.sin(theta)
            plt.plot(x, y, color='black', linewidth=1.0, zorder=10)

        text_x, text_y = center['x'], center['y'] - loop_radius * 1.8
        ha, va = 'center', 'top'

    elif orientation == 'vertical':
        start_y = center['y'] - total_length / 2
        x_center = center['x']

        rect = plt.Rectangle(
            (x_center - loop_radius, start_y),
            loop_radius * 2, total_length,
            facecolor='white',
            edgecolor='none',
            zorder=9.5
        )
        plt.gca().add_patch(rect)

        for i in range(num_loops):
            theta = np.linspace(0, np.pi, 100)
            y = start_y + i * loop_spacing + loop_radius * (1 - np.cos(theta))
            x = x_center + loop_radius * np.sin(theta)
            plt.plot(x, y, color='black', linewidth=1.0, zorder=10)

        text_x, text_y = center['x'] + loop_radius * 1.8, center['y']
        ha, va = 'left', 'center'

    plt.text(text_x, text_y, name, fontsize=6, ha=ha, va=va, color='blue', zorder=11)


def draw_voltage_source(center, name, orientation):
    radius = SCALE / 20
    arrow_length = radius * 1.2
    arrow_head_width = radius / 3

    circle = plt.Circle(
        (center['x'], center['y']),
        radius,
        edgecolor='black',
        facecolor='white',
        linewidth=1.0,
        zorder=10
    )
    plt.gca().add_patch(circle)

    rect = plt.Rectangle(
        (center['x'] - radius, center['y'] - radius),
        2 * radius, 2 * radius,
        facecolor='white',
        edgecolor='none',
        zorder=9.5
    )
    plt.gca().add_patch(rect)

    if orientation == 'horizontal':
        dx, dy = arrow_length, 0
        x_start = center['x'] - dx / 2
        y_start = center['y']
        text_x, text_y = center['x'], center['y'] - radius * 1.8
        ha, va = 'center', 'top'
    elif orientation == 'vertical':
        dx, dy = 0, -arrow_length
        x_start = center['x']
        y_start = center['y'] + abs(dy) / 2
        text_x, text_y = center['x'] + radius * 1.8, center['y']
        ha, va = 'left', 'center'

    plt.arrow(
        x_start,
        y_start,
        dx,
        dy,
        head_width=arrow_head_width,
        head_length=arrow_head_width,
        linewidth=1.0,
        color='black',
        length_includes_head=True,
        zorder=10
    )

    plt.text(text_x, text_y, name, fontsize=6, ha=ha, va=va, color='blue', zorder=11)


def draw_current_source(center, name, orientation):
    radius = SCALE / 20
    tick_size = radius * 0.6
    spacing = radius * 0.5

    circle = plt.Circle(
        (center['x'], center['y']),
        radius,
        edgecolor='black',
        facecolor='white',
        linewidth=1.0,
        zorder=10
    )
    plt.gca().add_patch(circle)

    rect = plt.Rectangle(
        (center['x'] - radius, center['y'] - radius),
        2 * radius, 2 * radius,
        facecolor='white',
        edgecolor='none',
        zorder=9.5
    )
    plt.gca().add_patch(rect)

    if orientation == 'horizontal':
        y = center['y']
        x1 = center['x'] - spacing / 2
        x2 = center['x'] + spacing / 2

        for x in [x1, x2]:
            plt.plot(
                [x - tick_size / 2, x, x - tick_size / 2],
                [y - tick_size / 2, y, y + tick_size / 2],
                color='black',
                linewidth=1.0,
                zorder=10
            )

        text_x, text_y = center['x'], center['y'] - radius * 1.8
        ha, va = 'center', 'top'

    elif orientation == 'vertical':
        x = center['x']
        y1 = center['y'] + spacing / 2
        y2 = center['y'] - spacing / 2

        for y in [y1, y2]:
            plt.plot(
                [x - tick_size / 2, x, x + tick_size / 2],
                [y + tick_size / 2, y, y + tick_size / 2],
                color='black',
                linewidth=1.0,
                zorder=10
            )

        text_x, text_y = center['x'] + radius * 1.8, center['y']
        ha, va = 'left', 'center'

    plt.text(text_x, text_y, name, fontsize=6, ha=ha, va=va, color='blue', zorder=11)


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
            plt.plot(coords['x'], coords['y'], 'ko', markersize=3)

        resistor_idx = 1
        capacity_idx = 1
        inductance_idx = 1
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
                                draw_resistor({'x': end['x'], 'y': current_position}, 'R' + str(resistor_idx), 'vertical')
                                resistor_idx += 1
                            elif element['type'] == 'capacity':
                                draw_capacitor({'x': end['x'], 'y': current_position}, 'C' + str(capacity_idx), 'vertical')
                                capacity_idx += 1
                            elif element['type'] == 'inductance':
                                draw_inductor({'x': end['x'], 'y': current_position}, 'L' + str(inductance_idx), 'vertical')
                                inductance_idx += 1
                            elif element['type'] == 'voltage_source':
                                draw_voltage_source({'x': end['x'], 'y': current_position}, 'V' + str(voltage_source_idx), 'vertical')
                                voltage_source_idx += 1
                            elif element['type'] == 'current_source':
                                draw_current_source({'x': end['x'], 'y': current_position}, 'I' + str(current_source_idx), 'vertical')
                                current_source_idx += 1
                            current_position += 2 * step
                    elif start['y'] == end['y']:
                        step = (abs(end['x'] - start['x']) / num_elements) / 2
                        current_position = min(end['x'], start['x']) + step
                        for element in segment_elements:
                            if element['type'] == 'resistor':
                                draw_resistor({'x': current_position, 'y': end['y']}, 'R' + str(resistor_idx), 'horizontal')
                                resistor_idx += 1
                            elif element['type'] == 'capacity':
                                draw_capacitor({'x': current_position, 'y': end['y']}, 'C' + str(capacity_idx), 'horizontal')
                                capacity_idx += 1
                            elif element['type'] == 'inductance':
                                draw_inductor({'x': current_position, 'y': end['y']}, 'L' + str(inductance_idx), 'horizontal')
                                inductance_idx += 1
                            elif element['type'] == 'voltage_source':
                                draw_voltage_source({'x': current_position, 'y': end['y']}, 'V' + str(voltage_source_idx), 'horizontal')
                                voltage_source_idx += 1
                            elif element['type'] == 'current_source':
                                draw_current_source({'x': current_position, 'y': end['y']}, 'I' + str(current_source_idx), 'horizontal')
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
                                elif element['type'] == 'capacity':
                                    draw_capacitor(pos, 'C' + str(capacity_idx), 'vertical')
                                    capacity_idx += 1
                                elif element['type'] == 'inductance':
                                    draw_inductor(pos, 'L' + str(inductance_idx), 'vertical')
                                    inductance_idx += 1
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
                                elif element['type'] == 'capacity':
                                    draw_capacitor(pos, 'C' + str(capacity_idx), 'horizontal')
                                    capacity_idx += 1
                                elif element['type'] == 'inductance':
                                    draw_inductor(pos, 'L' + str(inductance_idx), 'horizontal')
                                    inductance_idx += 1
                                elif element['type'] == 'voltage_source':
                                    draw_voltage_source(pos, 'V' + str(voltage_source_idx), 'horizontal')
                                    voltage_source_idx += 1
                                elif element['type'] == 'current_source':
                                    draw_current_source(pos, 'I' + str(current_source_idx), 'horizontal')
                                    current_source_idx += 1
                                current_position += 2 * step

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
