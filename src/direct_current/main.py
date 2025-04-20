import random
import matplotlib.pyplot as plt

from PIL import Image, PngImagePlugin
import io

from src.common.electric_circuit import ElectricCircuit
from src.direct_current.elements_places import ElementsPlacer
from src.direct_current.visualize_circuit import CircuitVisualize
from src.common.word_functions import add_schemes_to_word

from conf.config import SCALE


SCHEMES_FOLDER = 'schemes'


def compare_topologies(circuit_topology_1, circuit_topology_2):
    def normalize_connection(node_a, node_b):
        return "->".join(sorted([node_a, node_b]))

    def get_topology_representation(circuit_topology):
        representation = {}
        for conn_name, conn_coords in circuit_topology.nodes_connections.items():
            node1, node2 = conn_name.split('->')
            key = normalize_connection(node1, node2)
            if key not in representation:
                representation[key] = 0
            representation[key] += len(conn_coords)
        return representation

    rep1 = get_topology_representation(circuit_topology_1)
    rep2 = get_topology_representation(circuit_topology_2)

    return rep1 == rep2


def compare_layouts(circuit_layout_1, circuit_layout_2):
    absolutely_unique = True
    for connection_name_1, connection_params_1 in circuit_layout_1.items():
        for connection_name_2, connection_params_2 in circuit_layout_2.items():
            splited_name_1 = connection_name_1.split('->')
            if (connection_name_2 == connection_params_1) or (
                    connection_name_2 == f"{splited_name_1[1]}->{splited_name_1[0]}"):
                if len(connection_params_1) == len(connection_params_2):
                    connection_elements_1 = []
                    connection_elements_2 = []

                    for sub_connection in connection_params_1:
                        connection_elements_1.append(sub_connection[0]['elements'])

                    for sub_connection in connection_params_2:
                        connection_elements_2.append(sub_connection[0]['elements'])

                    set1 = {tuple(sorted(tuple(element.items()) for element in sub_list))
                            for sub_list in connection_elements_1}
                    set2 = {tuple(sorted(tuple(element.items()) for element in sub_list))
                            for sub_list in connection_elements_2}

                    if set1 != set2:
                        absolutely_unique = False

    return absolutely_unique


def generate_schemes_set(nodes_num, branches_num, voltage_sources_num, current_sources_num, resistors_num):
    template_two_nodes_1 = {'node1': {'x': 0, 'y': 0},
                            'node2': {'x': SCALE, 'y': 0}}

    template_three_nodes_1 = {'node1': {'x': 0, 'y': 0},
                              'node2': {'x': 0, 'y': SCALE},
                              'node3': {'x': SCALE, 'y': SCALE}}

    template_four_nodes_1 = {'node1': {'x': 0, 'y': 0},
                             'node2': {'x': 0, 'y': SCALE},
                             'node3': {'x': SCALE, 'y': SCALE},
                             'node4': {'x': SCALE, 'y': 0}}

    template_four_nodes_2 = {'node1': {'x': 0, 'y': SCALE},
                             'node2': {'x': SCALE, 'y': SCALE},
                             'node3': {'x': 2 * SCALE, 'y': SCALE},
                             'node4': {'x': SCALE, 'y': 0}}

    def get_unique_topologies(topologies, needed_count):
        unique = []
        for topo in topologies:
            if all(not compare_topologies(topo, u) for u in unique):
                unique.append(topo)
                if len(unique) >= needed_count:
                    break
        return unique

    circuits_topologies = []

    if nodes_num == 2:
        raw_topologies = [ElectricCircuit(branches_num=branches_num, nodes=template_two_nodes_1).create_nodes_connections() for _ in range(100)]
        circuits_topologies = get_unique_topologies(raw_topologies, 30)

    elif nodes_num == 3:
        raw_topologies = [ElectricCircuit(branches_num=branches_num, nodes=template_three_nodes_1).create_nodes_connections() for _ in range(500)]
        circuits_topologies = get_unique_topologies(raw_topologies, 30)

    elif nodes_num == 4:
        circuits_topologies_1 = [ElectricCircuit(branches_num=branches_num, nodes=template_four_nodes_1).create_nodes_connections() for _ in range(300)]
        circuits_topologies_2 = [ElectricCircuit(branches_num=branches_num, nodes=template_four_nodes_2).create_nodes_connections() for _ in range(300)]

        unique_1 = get_unique_topologies(circuits_topologies_1, 15)
        unique_2 = get_unique_topologies(circuits_topologies_2, 15)
        circuits_topologies = unique_1 + unique_2

        if len(circuits_topologies) < 30:
            print(f'[Warning] Удалось сгенерировать только {len(circuits_topologies)} уникальных топологий.')
            print(f'[Info] Добираем ещё {30 - len(circuits_topologies)} топологий случайным образом (с возможными повторами).')
            all_topos = circuits_topologies_1 + circuits_topologies_2
            while len(circuits_topologies) < 30:
                circuits_topologies.append(random.choice(all_topos))

        random.shuffle(circuits_topologies)

    if len(circuits_topologies) < 30:
        print(f'[Warning] Удалось сгенерировать только {len(circuits_topologies)} уникальных топологий.')
        print(f'[Info] Добираем ещё {30 - len(circuits_topologies)} топологий случайным образом (с возможными повторами).')
        while len(circuits_topologies) < 30:
            circuits_topologies.append(random.choice(raw_topologies))

    circuits = []
    circuits_topologies_paired = []

    for circuit_topology in circuits_topologies:
        placed_circuit = ElementsPlacer(circuit_topology,
                                        voltage_sources_num,
                                        current_sources_num,
                                        resistors_num).place_elements()
        circuits.append(placed_circuit)
        circuits_topologies_paired.append((circuit_topology, placed_circuit))

    unique_schemes = []

    for i in range(len(circuits_topologies_paired)):
        topology_1, circuit_1 = circuits_topologies_paired[i]
        is_unique = True

        for existing_topology, existing_circuit in unique_schemes:
            if compare_layouts(circuit_1.layout, existing_circuit.layout) and compare_topologies(topology_1, existing_topology):
                is_unique = False
                break

        if is_unique:
            unique_schemes.append((topology_1, circuit_1))

    index = 1
    for topology, circuit in circuits_topologies_paired:
        visualizer = CircuitVisualize(circuit, topology)
        visualizer.visualize()

        buf = io.BytesIO()
        fig = plt.gcf()
        fig.savefig(buf, format='png', dpi=300, bbox_inches='tight', pad_inches=0)
        plt.close(fig)

        buf.seek(0)
        img = Image.open(buf)

        meta = PngImagePlugin.PngInfo()
        meta.add_text("voltage_sources_num", str(voltage_sources_num))
        meta.add_text("current_sources_num", str(current_sources_num))
        meta.add_text("resistors_num", str(resistors_num))

        img.save(f'{SCHEMES_FOLDER}/scheme_{index}.png', pnginfo=meta)

        index += 1

    if len(unique_schemes) < 30:
        return {"code": "warning", "message": f'Удалось сгенерировать только {len(unique_schemes)} уникальных схем'}

    return {"code": "success", "message": "Набор схем успешно сгенерирован"}


def generate_direct_current_schemes_set(nodes_num, branches_num, voltage_sources_num, current_sources_num, resistors_num):
    status = generate_schemes_set(
        nodes_num=nodes_num,
        branches_num=branches_num,
        voltage_sources_num=voltage_sources_num,
        current_sources_num=current_sources_num,
        resistors_num=resistors_num
    )

    if status['code'] == "error":
        return status

    add_schemes_to_word(
        scheme_type="direct_current"
    )

    return status
