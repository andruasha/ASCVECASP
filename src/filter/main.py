import matplotlib.pyplot as plt
import numpy as np
import random

from src.common.draw_functions import draw_resistor, draw_capacitor, draw_inductor
from src.common.word_functions import add_schemes_to_word

from PIL import Image, PngImagePlugin
import io

from conf.config import SCALE

SCHEMES_FOLDER = 'schemes'


def generate_filter_scheme_topology(scheme_type):
    all_nodes = {}
    scheme_nodes = {}
    quadripole_nodes = {}
    scheme_layout = {}
    if scheme_type == 'G':
        all_nodes = {
            'node1': {'x': 0, 'y': SCALE},
            'node2': {'x': SCALE, 'y': SCALE},
            'node3': {'x': 3 * SCALE / 2, 'y': SCALE},
            'node4': {'x': 0, 'y': 0},
            'node5': {'x': SCALE, 'y': 0},
            'node6': {'x': 3 * SCALE / 2, 'y': 0}
        }

        scheme_nodes = {
            'node2': {'x': SCALE, 'y': SCALE},
            'node5': {'x': SCALE, 'y': 0}
        }

        quadripole_nodes = {
            'node1': {'x': 0, 'y': SCALE},
            'node3': {'x': 3 * SCALE / 2, 'y': SCALE},
            'node4': {'x': 0, 'y': 0},
            'node6': {'x': 3 * SCALE / 2, 'y': 0}
        }

        scheme_layout = {
            'node1->node2': [
                {
                    'connection_coords': [
                        all_nodes['node1'],
                        all_nodes['node2']
                    ],
                    'elements': []
                }
            ],
            'node2->node3': [
                {
                    'connection_coords': [
                        all_nodes['node2'],
                        all_nodes['node3']
                    ]
                }
            ],
            'node4->node5': [
                {
                    'connection_coords': [
                        all_nodes['node4'],
                        all_nodes['node5']
                    ]
                }
            ],
            'node5->node6': [
                {
                    'connection_coords': [
                        all_nodes['node5'],
                        all_nodes['node6']
                    ]
                }
            ],
            'node2->node5': [
                {
                    'connection_coords': [
                        all_nodes['node2'],
                        all_nodes['node5']
                    ],
                    'elements': []
                }
            ]
        }

    elif scheme_type == 'P':
        all_nodes = {
            'node1': {'x': 0, 'y': SCALE},
            'node2': {'x': SCALE / 2, 'y': SCALE},
            'node3': {'x': 3 * SCALE / 2, 'y': SCALE},
            'node4': {'x': 2 * SCALE, 'y': SCALE},
            'node5': {'x': 0, 'y': 0},
            'node6': {'x': SCALE / 2, 'y': 0},
            'node7': {'x': 3 * SCALE / 2, 'y': 0},
            'node8': {'x': 2 * SCALE, 'y': 0}
        }

        scheme_nodes = {
            'node2': {'x': SCALE / 2, 'y': SCALE},
            'node3': {'x': 3 * SCALE / 2, 'y': SCALE},
            'node6': {'x': SCALE / 2, 'y': 0},
            'node7': {'x': 3 * SCALE / 2, 'y': 0}
        }

        quadripole_nodes = {
            'node1': {'x': 0, 'y': SCALE},
            'node4': {'x': 2 * SCALE, 'y': SCALE},
            'node5': {'x': 0, 'y': 0},
            'node8': {'x': 2 * SCALE, 'y': 0}
        }

        scheme_layout = {
            'node1->node2': [
                {
                    'connection_coords': [
                        all_nodes['node1'],
                        all_nodes['node2']
                    ]
                }
            ],
            'node2->node3': [
                {
                    'connection_coords': [
                        all_nodes['node2'],
                        all_nodes['node3']
                    ],
                    'elements': []
                }
            ],
            'node3->node4': [
                {
                    'connection_coords': [
                        all_nodes['node3'],
                        all_nodes['node4']
                    ]
                }
            ],
            'node5->node6': [
                {
                    'connection_coords': [
                        all_nodes['node5'],
                        all_nodes['node6']
                    ]
                }
            ],
            'node6->node7': [
                {
                    'connection_coords': [
                        all_nodes['node6'],
                        all_nodes['node7']
                    ]
                }
            ],
            'node7->node8': [
                {
                    'connection_coords': [
                        all_nodes['node7'],
                        all_nodes['node8']
                    ]
                }
            ],
            'node2->node6': [
                {
                    'connection_coords': [
                        all_nodes['node2'],
                        all_nodes['node6']
                    ],
                    'elements': []
                }
            ],
            'node3->node7': [
                {
                    'connection_coords': [
                        all_nodes['node3'],
                        all_nodes['node7']
                    ],
                    'elements': []
                }
            ]
        }

    elif scheme_type == 'T':
        all_nodes = {
            'node1': {'x': 0, 'y': SCALE},
            'node2': {'x': SCALE, 'y': SCALE},
            'node3': {'x': 2 * SCALE, 'y': SCALE},
            'node4': {'x': 0, 'y': 0},
            'node5': {'x': SCALE, 'y': 0},
            'node6': {'x': 2 * SCALE, 'y': 0}
        }

        scheme_nodes = {
            'node2': {'x': SCALE, 'y': SCALE},
            'node5': {'x': SCALE, 'y': 0}
        }

        quadripole_nodes = {
            'node1': {'x': 0, 'y': SCALE},
            'node3': {'x': 2 * SCALE, 'y': SCALE},
            'node4': {'x': 0, 'y': 0},
            'node6': {'x': 2 * SCALE, 'y': 0}
        }

        scheme_layout = {
            'node1->node2': [
                {
                    'connection_coords': [
                        all_nodes['node1'],
                        all_nodes['node2']
                    ],
                    'elements': []
                }
            ],
            'node2->node3': [
                {
                    'connection_coords': [
                        all_nodes['node2'],
                        all_nodes['node3']
                    ],
                    'elements': []
                }
            ],
            'node4->node5': [
                {
                    'connection_coords': [
                        all_nodes['node4'],
                        all_nodes['node5']
                    ]
                }
            ],
            'node5->node6': [
                {
                    'connection_coords': [
                        all_nodes['node5'],
                        all_nodes['node6']
                    ]
                }
            ],
            'node2->node5': [
                {
                    'connection_coords': [
                        all_nodes['node2'],
                        all_nodes['node5']
                    ],
                    'elements': []
                }
            ],
        }

    elif scheme_type == 'T_bridge':
        all_nodes = {
            'node1': {'x': 0, 'y': SCALE},
            'node2': {'x': SCALE / 2, 'y': SCALE},
            'node3': {'x': 3 * SCALE / 2, 'y': SCALE},
            'node4': {'x': 2 * SCALE, 'y': SCALE},
            'node5': {'x': 0, 'y': 0},
            'node6': {'x': SCALE / 2, 'y': 0},
            'node7': {'x': 3 * SCALE / 2, 'y': 0},
            'node8': {'x': 2 * SCALE, 'y': 0}
        }

        scheme_nodes = {
            'node2': {'x': SCALE / 2, 'y': SCALE},
            'node3': {'x': 3 * SCALE / 2, 'y': SCALE},
            'node6': {'x': SCALE / 2, 'y': 0},
            'node7': {'x': 3 * SCALE / 2, 'y': 0}
        }

        quadripole_nodes = {
            'node1': {'x': 0, 'y': SCALE},
            'node4': {'x': 2 * SCALE, 'y': SCALE},
            'node5': {'x': 0, 'y': 0},
            'node8': {'x': 2 * SCALE, 'y': 0}
        }

        scheme_layout = {
            'node1->node2': [
                {
                    'connection_coords': [
                        all_nodes['node1'],
                        all_nodes['node2']
                    ]
                }
            ],
            'node2->node3': [
                {
                    'connection_coords': [
                        all_nodes['node2'],
                        all_nodes['node3']
                    ],
                    'elements': []
                }
            ],
            'node3->node4': [
                {
                    'connection_coords': [
                        all_nodes['node3'],
                        all_nodes['node4']
                    ]
                }
            ],
            'node5->node6': [
                {
                    'connection_coords': [
                        all_nodes['node5'],
                        all_nodes['node6']
                    ]
                }
            ],
            'node6->node7': [
                {
                    'connection_coords': [
                        all_nodes['node6'],
                        all_nodes['node7']
                    ],
                    'elements': []
                }
            ],
            'node7->node8': [
                {
                    'connection_coords': [
                        all_nodes['node7'],
                        all_nodes['node8']
                    ]
                }
            ],
            'node2->node7': [
                {
                    'connection_coords': [
                        all_nodes['node2'],
                        all_nodes['node7']
                    ],
                    'elements': []
                }
            ],
            'node3->node6': [
                {
                    'connection_coords': [
                        all_nodes['node3'],
                        all_nodes['node6']
                    ],
                    'elements': []
                }
            ]
        }

    elif scheme_type == 'T_back_coupling':
        all_nodes = {
            'node1': {'x': 0, 'y': SCALE},
            'node2': {'x': SCALE / 2, 'y': SCALE},
            'node3': {'x': 3 * SCALE / 2, 'y': SCALE},
            'node4': {'x': 2 * SCALE, 'y': 3 * SCALE / 2},
            'node5': {'x': 3 * SCALE, 'y': SCALE},
            'node6': {'x': 7 * SCALE / 2, 'y': SCALE},
            'node7': {'x': 0, 'y': 0},
            'node8': {'x': 3 * SCALE / 2, 'y': 0},
            'node9': {'x': 2 * SCALE, 'y': 0},
            'node10': {'x': 7 * SCALE / 2, 'y': 0}
        }

        scheme_nodes = {
            'node2': {'x': SCALE / 2, 'y': SCALE},
            'node3': {'x': 3 * SCALE / 2, 'y': SCALE},
            'node4': {'x': 2 * SCALE, 'y': 3 * SCALE / 2},
            'node5': {'x': 3 * SCALE, 'y': SCALE},
            'node8': {'x': 3 * SCALE / 2, 'y': 0},
            'node9': {'x': 2 * SCALE, 'y': 0},
        }

        quadripole_nodes = {
            'node1': {'x': 0, 'y': SCALE},
            'node6': {'x': 7 * SCALE / 2, 'y': SCALE},
            'node7': {'x': 0, 'y': 0},
            'node10': {'x': 7 * SCALE / 2, 'y': 0}
        }

        scheme_layout = {
            'node1->node2': [
                {
                    'connection_coords': [
                        all_nodes['node1'],
                        all_nodes['node2']
                    ]
                }
            ],
            'node2->node3': [
                {
                    'connection_coords': [
                        all_nodes['node2'],
                        all_nodes['node3']
                    ],
                    'elements': []
                }
            ],
            'node3->node5': [
                {
                    'connection_coords': [
                        all_nodes['node3'],
                        all_nodes['node5']
                    ],
                    'elements': []
                }
            ],
            'node5->node6': [
                {
                    'connection_coords': [
                        all_nodes['node5'],
                        all_nodes['node6']
                    ]
                }
            ],
            'node2->node4': [
                {
                    'connection_coords': [
                        all_nodes['node2'],
                        {'x': all_nodes['node2']['x'], 'y': all_nodes['node4']['y']},
                        all_nodes['node4'],
                    ],
                    'elements': []
                }
            ],
            'node4->node5': [
                {
                    'connection_coords': [
                        all_nodes['node4'],
                        {'x': all_nodes['node5']['x'], 'y': all_nodes['node4']['y']},
                        all_nodes['node5']
                    ],
                    'elements': []
                }
            ],
            'node7->node8': [
                {
                    'connection_coords': [
                        all_nodes['node7'],
                        all_nodes['node8']
                    ]
                }
            ],
            'node8->node9': [
                {
                    'connection_coords': [
                        all_nodes['node8'],
                        all_nodes['node9']
                    ]
                }
            ],
            'node9->node10': [
                {
                    'connection_coords': [
                        all_nodes['node9'],
                        all_nodes['node10']
                    ]
                }
            ],
            'node3->node8': [
                {
                    'connection_coords': [
                        all_nodes['node3'],
                        all_nodes['node8']
                    ],
                    'elements': []
                }
            ],
            'node4->node9': [
                {
                    'connection_coords': [
                        all_nodes['node4'],
                        all_nodes['node9']
                    ],
                    'elements': []
                }
            ]
        }

    return scheme_nodes, quadripole_nodes, scheme_layout


def visualise_filter_scheme(scheme_nodes, quadripole_nodes, scheme_layout):
    plt.figure(figsize=(5, 5))
    plt.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray')
    plt.xticks(range(-13, 14, 1))
    plt.yticks(range(-13, 14, 1))
    plt.xlim(-13, 13)
    plt.ylim(-13, 13)
    plt.axis('equal')

    for node, coords in scheme_nodes.items():
        plt.plot(coords['x'], coords['y'], 'ko', markersize=3)
    for node, coords in quadripole_nodes.items():
        plt.plot(coords['x'], coords['y'], 'ro', markersize=3, zorder=11)

    resistor_idx = 1
    capacitor_idx = 1
    inductor_idx = 1

    for c_name, connections in scheme_layout.items():
        for segment in connections:
            coords = segment['connection_coords']
            for i in range(len(coords) - 1):
                start = coords[i]
                end = coords[i + 1]
                plt.plot([start['x'], end['x']], [start['y'], end['y']], 'k-', linewidth=1)

            if 'elements' not in segment:
                continue

            elements = segment['elements']
            num_elements = len(elements)

            if num_elements == 0:
                continue

            lines = []
            for i in range(len(coords) - 1):
                lines.append((coords[i], coords[i + 1]))

            num_lines = len(lines)
            elements_per_line = num_elements // num_lines
            extra = num_elements % num_lines

            element_iter = iter(elements)

            for idx, (start, end) in enumerate(lines):
                count = elements_per_line + (1 if idx < extra else 0)
                if count == 0:
                    continue

                dx = end['x'] - start['x']
                dy = end['y'] - start['y']

                if dx == 0 and dy != 0:
                    step = (abs(dy) / count) / 2
                    pos_y = min(start['y'], end['y']) + step
                    for _ in range(count):
                        pos = {'x': start['x'], 'y': pos_y}
                        el = next(element_iter)
                        if el == 'resistor':
                            draw_resistor(pos, f'R{resistor_idx}', 'vertical')
                            resistor_idx += 1
                        elif el == 'capacitor':
                            draw_capacitor(pos, f'C{capacitor_idx}', 'vertical')
                            capacitor_idx += 1
                        elif el == 'inductor':
                            draw_inductor(pos, f'L{inductor_idx}', 'vertical')
                            inductor_idx += 1
                        pos_y += 2 * step

                elif dy == 0 and dx != 0:
                    step = (abs(dx) / count) / 2
                    pos_x = min(start['x'], end['x']) + step
                    for _ in range(count):
                        pos = {'x': pos_x, 'y': start['y']}
                        el = next(element_iter)
                        if el == 'resistor':
                            draw_resistor(pos, f'R{resistor_idx}', 'horizontal')
                            resistor_idx += 1
                        elif el == 'capacitor':
                            draw_capacitor(pos, f'C{capacitor_idx}', 'horizontal')
                            capacitor_idx += 1
                        elif el == 'inductor':
                            draw_inductor(pos, f'L{inductor_idx}', 'horizontal')
                            inductor_idx += 1
                        pos_x += 2 * step

                else:
                    length = np.sqrt(dx ** 2 + dy ** 2)
                    angle = np.arctan2(dy, dx)

                    if abs(angle) < np.pi / 2:
                        orientation = 'diagonal' if dy > 0 else '-diagonal'
                    else:
                        orientation = '-diagonal' if dy > 0 else 'diagonal'

                    valid_t = np.linspace(0.1, 0.9, count * 2)
                    valid_t = [t for t in valid_t if t < 0.4 or t > 0.6][:count]

                    for t in valid_t:
                        pos_x = start['x'] + t * dx
                        pos_y = start['y'] + t * dy
                        pos = {'x': pos_x, 'y': pos_y}
                        el = next(element_iter)
                        if el == 'resistor':
                            draw_resistor(pos, f'R{resistor_idx}', orientation)
                            resistor_idx += 1
                        elif el == 'capacitor':
                            draw_capacitor(pos, f'C{capacitor_idx}', orientation)
                            capacitor_idx += 1
                        elif el == 'inductor':
                            draw_inductor(pos, f'L{inductor_idx}', orientation)
                            inductor_idx += 1

    plt.axis('off')


def generate_filter_schemes_set(scheme_type, filter_type, save_path):
    schemes = []

    if filter_type == 'LPF':
        if scheme_type == 'G':
            for _ in range(11):
                scheme_nodes, quadripole_nodes, scheme_layout = generate_filter_scheme_topology(
                    scheme_type=scheme_type
                )
                scheme_layout['node1->node2'][0]['elements'].append('resistor')
                scheme_layout['node2->node5'][0]['elements'].append('capacitor')
                schemes.append({
                    "scheme_nodes": scheme_nodes,
                    "quadripole_nodes": quadripole_nodes,
                    "scheme_layout": scheme_layout
                })

            for _ in range(11):
                scheme_nodes, quadripole_nodes, scheme_layout = generate_filter_scheme_topology(
                    scheme_type=scheme_type
                )
                scheme_layout['node1->node2'][0]['elements'].append('inductor')
                scheme_layout['node2->node5'][0]['elements'].append('resistor')
                schemes.append({
                    "scheme_nodes": scheme_nodes,
                    "quadripole_nodes": quadripole_nodes,
                    "scheme_layout": scheme_layout
                })

            for _ in range(11):
                scheme_nodes, quadripole_nodes, scheme_layout = generate_filter_scheme_topology(
                    scheme_type=scheme_type
                )
                scheme_layout['node1->node2'][0]['elements'].append('inductor')
                scheme_layout['node2->node5'][0]['elements'].append('capacitor')
                schemes.append({
                    "scheme_nodes": scheme_nodes,
                    "quadripole_nodes": quadripole_nodes,
                    "scheme_layout": scheme_layout
                })

        if scheme_type == 'P':
            for _ in range(11):
                scheme_nodes, quadripole_nodes, scheme_layout = generate_filter_scheme_topology(
                    scheme_type=scheme_type
                )
                scheme_layout['node2->node3'][0]['elements'].append('resistor')
                scheme_layout['node2->node6'][0]['elements'].append('capacitor')
                scheme_layout['node3->node7'][0]['elements'].append('capacitor')
                schemes.append({
                    "scheme_nodes": scheme_nodes,
                    "quadripole_nodes": quadripole_nodes,
                    "scheme_layout": scheme_layout
                })

            for _ in range(11):
                scheme_nodes, quadripole_nodes, scheme_layout = generate_filter_scheme_topology(
                    scheme_type=scheme_type
                )
                scheme_layout['node2->node3'][0]['elements'].append('inductor')
                scheme_layout['node2->node6'][0]['elements'].append('resistor')
                scheme_layout['node3->node7'][0]['elements'].append('resistor')
                schemes.append({
                    "scheme_nodes": scheme_nodes,
                    "quadripole_nodes": quadripole_nodes,
                    "scheme_layout": scheme_layout
                })

            for _ in range(11):
                scheme_nodes, quadripole_nodes, scheme_layout = generate_filter_scheme_topology(
                    scheme_type=scheme_type
                )
                scheme_layout['node2->node3'][0]['elements'].append('inductor')
                scheme_layout['node2->node6'][0]['elements'].append('capacitor')
                scheme_layout['node3->node7'][0]['elements'].append('capacitor')
                schemes.append({
                    "scheme_nodes": scheme_nodes,
                    "quadripole_nodes": quadripole_nodes,
                    "scheme_layout": scheme_layout
                })

        if scheme_type == 'T':
            for _ in range(11):
                scheme_nodes, quadripole_nodes, scheme_layout = generate_filter_scheme_topology(
                    scheme_type=scheme_type
                )
                scheme_layout['node1->node2'][0]['elements'].append('resistor')
                scheme_layout['node2->node3'][0]['elements'].append('resistor')
                scheme_layout['node2->node5'][0]['elements'].append('capacitor')
                schemes.append({
                    "scheme_nodes": scheme_nodes,
                    "quadripole_nodes": quadripole_nodes,
                    "scheme_layout": scheme_layout
                })

            for _ in range(11):
                scheme_nodes, quadripole_nodes, scheme_layout = generate_filter_scheme_topology(
                    scheme_type=scheme_type
                )
                scheme_layout['node1->node2'][0]['elements'].append('inductor')
                scheme_layout['node2->node3'][0]['elements'].append('inductor')
                scheme_layout['node2->node5'][0]['elements'].append('resistor')
                schemes.append({
                    "scheme_nodes": scheme_nodes,
                    "quadripole_nodes": quadripole_nodes,
                    "scheme_layout": scheme_layout
                })

            for _ in range(11):
                scheme_nodes, quadripole_nodes, scheme_layout = generate_filter_scheme_topology(
                    scheme_type=scheme_type
                )
                scheme_layout['node1->node2'][0]['elements'].append('inductor')
                scheme_layout['node2->node3'][0]['elements'].append('inductor')
                scheme_layout['node2->node5'][0]['elements'].append('capacitor')
                schemes.append({
                    "scheme_nodes": scheme_nodes,
                    "quadripole_nodes": quadripole_nodes,
                    "scheme_layout": scheme_layout
                })

    if filter_type == 'HPF':
        if scheme_type == 'G':
            for _ in range(11):
                scheme_nodes, quadripole_nodes, scheme_layout = generate_filter_scheme_topology(
                    scheme_type=scheme_type
                )
                scheme_layout['node1->node2'][0]['elements'].append('capacitor')
                scheme_layout['node2->node5'][0]['elements'].append('resistor')
                schemes.append({
                    "scheme_nodes": scheme_nodes,
                    "quadripole_nodes": quadripole_nodes,
                    "scheme_layout": scheme_layout
                })

            for _ in range(11):
                scheme_nodes, quadripole_nodes, scheme_layout = generate_filter_scheme_topology(
                    scheme_type=scheme_type
                )
                scheme_layout['node1->node2'][0]['elements'].append('resistor')
                scheme_layout['node2->node5'][0]['elements'].append('inductor')
                schemes.append({
                    "scheme_nodes": scheme_nodes,
                    "quadripole_nodes": quadripole_nodes,
                    "scheme_layout": scheme_layout
                })

            for _ in range(11):
                scheme_nodes, quadripole_nodes, scheme_layout = generate_filter_scheme_topology(
                    scheme_type=scheme_type
                )
                scheme_layout['node1->node2'][0]['elements'].append('capacitor')
                scheme_layout['node2->node5'][0]['elements'].append('inductor')
                schemes.append({
                    "scheme_nodes": scheme_nodes,
                    "quadripole_nodes": quadripole_nodes,
                    "scheme_layout": scheme_layout
                })

        if scheme_type == 'P':
            for _ in range(11):
                scheme_nodes, quadripole_nodes, scheme_layout = generate_filter_scheme_topology(
                    scheme_type=scheme_type
                )
                scheme_layout['node2->node3'][0]['elements'].append('capacitor')
                scheme_layout['node2->node6'][0]['elements'].append('resistor')
                scheme_layout['node3->node7'][0]['elements'].append('resistor')
                schemes.append({
                    "scheme_nodes": scheme_nodes,
                    "quadripole_nodes": quadripole_nodes,
                    "scheme_layout": scheme_layout
                })

            for _ in range(11):
                scheme_nodes, quadripole_nodes, scheme_layout = generate_filter_scheme_topology(
                    scheme_type=scheme_type
                )
                scheme_layout['node2->node3'][0]['elements'].append('resistor')
                scheme_layout['node2->node6'][0]['elements'].append('inductor')
                scheme_layout['node3->node7'][0]['elements'].append('inductor')
                schemes.append({
                    "scheme_nodes": scheme_nodes,
                    "quadripole_nodes": quadripole_nodes,
                    "scheme_layout": scheme_layout
                })

            for _ in range(11):
                scheme_nodes, quadripole_nodes, scheme_layout = generate_filter_scheme_topology(
                    scheme_type=scheme_type
                )
                scheme_layout['node2->node3'][0]['elements'].append('capacitor')
                scheme_layout['node2->node6'][0]['elements'].append('inductor')
                scheme_layout['node3->node7'][0]['elements'].append('inductor')
                schemes.append({
                    "scheme_nodes": scheme_nodes,
                    "quadripole_nodes": quadripole_nodes,
                    "scheme_layout": scheme_layout
                })

        if scheme_type == 'T':
            for _ in range(11):
                scheme_nodes, quadripole_nodes, scheme_layout = generate_filter_scheme_topology(
                    scheme_type=scheme_type
                )
                scheme_layout['node1->node2'][0]['elements'].append('capacitor')
                scheme_layout['node2->node3'][0]['elements'].append('capacitor')
                scheme_layout['node2->node5'][0]['elements'].append('resistor')
                schemes.append({
                    "scheme_nodes": scheme_nodes,
                    "quadripole_nodes": quadripole_nodes,
                    "scheme_layout": scheme_layout
                })

            for _ in range(11):
                scheme_nodes, quadripole_nodes, scheme_layout = generate_filter_scheme_topology(
                    scheme_type=scheme_type
                )
                scheme_layout['node1->node2'][0]['elements'].append('resistor')
                scheme_layout['node2->node3'][0]['elements'].append('resistor')
                scheme_layout['node2->node5'][0]['elements'].append('inductor')
                schemes.append({
                    "scheme_nodes": scheme_nodes,
                    "quadripole_nodes": quadripole_nodes,
                    "scheme_layout": scheme_layout
                })

            for _ in range(11):
                scheme_nodes, quadripole_nodes, scheme_layout = generate_filter_scheme_topology(
                    scheme_type=scheme_type
                )
                scheme_layout['node1->node2'][0]['elements'].append('capacitor')
                scheme_layout['node2->node3'][0]['elements'].append('capacitor')
                scheme_layout['node2->node5'][0]['elements'].append('inductor')
                schemes.append({
                    "scheme_nodes": scheme_nodes,
                    "quadripole_nodes": quadripole_nodes,
                    "scheme_layout": scheme_layout
                })

    if filter_type == 'BPF':
        if scheme_type == 'G':
            for _ in range(31):
                scheme_nodes, quadripole_nodes, scheme_layout = generate_filter_scheme_topology(
                    scheme_type=scheme_type
                )
                scheme_layout['node1->node2'][0]['elements'].append('inductor')
                scheme_layout['node1->node2'][0]['elements'].append('capacitor')
                scheme_layout['node2->node5'][0]['elements'].append('resistor')
                schemes.append({
                    "scheme_nodes": scheme_nodes,
                    "quadripole_nodes": quadripole_nodes,
                    "scheme_layout": scheme_layout
                })

        if scheme_type == 'P':
            for _ in range(31):
                scheme_nodes, quadripole_nodes, scheme_layout = generate_filter_scheme_topology(
                    scheme_type=scheme_type
                )
                scheme_layout['node2->node3'][0]['elements'].append('capacitor')
                scheme_layout['node2->node3'][0]['elements'].append('resistor')
                scheme_layout['node2->node6'][0]['elements'].append('resistor')
                scheme_layout['node3->node7'][0]['elements'].append('capacitor')
                schemes.append({
                    "scheme_nodes": scheme_nodes,
                    "quadripole_nodes": quadripole_nodes,
                    "scheme_layout": scheme_layout
                })

        if scheme_type == 'T':
            for _ in range(31):
                scheme_nodes, quadripole_nodes, scheme_layout = generate_filter_scheme_topology(
                    scheme_type=scheme_type
                )
                scheme_layout['node1->node2'][0]['elements'].append('resistor')
                scheme_layout['node2->node3'][0]['elements'].append('inductor')
                scheme_layout['node2->node5'][0]['elements'].append('inductor')
                schemes.append({
                    "scheme_nodes": scheme_nodes,
                    "quadripole_nodes": quadripole_nodes,
                    "scheme_layout": scheme_layout
                })

    if filter_type == 'BSF':
        if scheme_type == 'G':
            for _ in range(31):
                scheme_nodes, quadripole_nodes, scheme_layout = generate_filter_scheme_topology(
                    scheme_type=scheme_type
                )
                scheme_layout['node1->node2'][0]['elements'].append('resistor')
                scheme_layout['node2->node5'][0]['elements'].append('inductor')
                scheme_layout['node2->node5'][0]['elements'].append('capacitor')
                schemes.append({
                    "scheme_nodes": scheme_nodes,
                    "quadripole_nodes": quadripole_nodes,
                    "scheme_layout": scheme_layout
                })

        if scheme_type == 'T_back_coupling':
            for _ in range(31):
                scheme_nodes, quadripole_nodes, scheme_layout = generate_filter_scheme_topology(
                    scheme_type=scheme_type
                )
                scheme_layout['node2->node3'][0]['elements'].append('capacitor')
                scheme_layout['node3->node5'][0]['elements'].append('capacitor')
                scheme_layout['node2->node4'][0]['elements'].append('resistor')
                scheme_layout['node4->node5'][0]['elements'].append('resistor')
                scheme_layout['node3->node8'][0]['elements'].append('resistor')
                scheme_layout['node4->node9'][0]['elements'].append('capacitor')
                schemes.append({
                    "scheme_nodes": scheme_nodes,
                    "quadripole_nodes": quadripole_nodes,
                    "scheme_layout": scheme_layout
                })

    status = {"code": "success", "message": "Набор схем успешно сгенерирован"}
    unique_schemes = []

    for scheme in schemes:
        if len(unique_schemes) == 30:
            break
        if scheme not in unique_schemes:
            unique_schemes.append(scheme)

    if len(unique_schemes) < 30:
        status = {"code": "warning", "message": f'Удалось сгенерировать только {len(unique_schemes)} уникальных схем'}
        print(f'[Warning] Удалось сгенерировать только {len(unique_schemes)} уникальных схем')
        while len(unique_schemes) < 30:
            random_scheme = random.choice(schemes)
            unique_schemes.append(random_scheme)

    random.shuffle(unique_schemes)

    for idx, scheme in enumerate(unique_schemes, start=1):
        resistors_num = 0
        capacitors_num = 0
        inductors_num = 0

        for branch in scheme["scheme_layout"].values():
            if 'elements' in branch[0]:
                for element in branch[0]['elements']:
                    if element == 'resistor':
                        resistors_num += 1
                    elif element == 'capacitor':
                        capacitors_num += 1
                    elif element == 'inductor':
                        inductors_num += 1

        visualise_filter_scheme(
            scheme_nodes=scheme["scheme_nodes"],
            quadripole_nodes=scheme["quadripole_nodes"],
            scheme_layout=scheme["scheme_layout"]
        )

        buf = io.BytesIO()
        fig = plt.gcf()
        fig.savefig(buf, format='png', dpi=300, bbox_inches='tight', pad_inches=0)
        plt.close(fig)

        buf.seek(0)
        img = Image.open(buf)

        meta = PngImagePlugin.PngInfo()
        meta.add_text("voltage_sources_num", str(0))
        meta.add_text("current_sources_num", str(0))
        meta.add_text("resistors_num", str(resistors_num))
        meta.add_text("capacitors_num", str(capacitors_num))
        meta.add_text("inductors_num", str(inductors_num))

        img.save(f'{save_path}/{SCHEMES_FOLDER}/scheme_{idx}.png', pnginfo=meta)

    add_schemes_to_word(
        scheme_type="filter",
        save_path=save_path
    )

    return status
