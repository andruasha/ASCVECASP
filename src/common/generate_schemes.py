import random
import io
import os
import matplotlib.pyplot as plt
from PIL import Image, PngImagePlugin
from conf.config import SCALE
from src.common.compare_functions import compare_topologies, compare_layouts
from src.common.electric_circuit import ElectricCircuit
from src.common.elements_places import ElementsPlacer
from src.common.visualize_circuit import CircuitVisualize


SCHEMES_FOLDER = 'schemes'


def generate_schemes_set(nodes_num, branches_num, voltage_sources_num, current_sources_num, resistors_num, inductors_num, capacitors_num, scheme_type, save_path):

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
        raw_topologies = [ElectricCircuit(branches_num=branches_num, nodes=template_two_nodes_1).create_nodes_connections() for _ in range(30)]
        circuits_topologies = get_unique_topologies(raw_topologies, 30)

    elif nodes_num == 3:
        raw_topologies = [ElectricCircuit(branches_num=branches_num, nodes=template_three_nodes_1).create_nodes_connections() for _ in range(500)]
        circuits_topologies = get_unique_topologies(raw_topologies, 30)

    elif nodes_num == 4:
        circuits_topologies_1 = [ElectricCircuit(branches_num=branches_num, nodes=template_four_nodes_1).create_nodes_connections() for _ in range(500)]
        circuits_topologies_2 = [ElectricCircuit(branches_num=branches_num, nodes=template_four_nodes_2).create_nodes_connections() for _ in range(500)]

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
        placed_circuit = ElementsPlacer(
            circuit_topology=circuit_topology,
            voltage_sources_num=voltage_sources_num,
            current_sources_num=current_sources_num,
            resistors_num=resistors_num,
            inductors_num=inductors_num,
            capacitors_num=capacitors_num,
            scheme_type=scheme_type
        ).place_elements()

        if isinstance(placed_circuit, dict):
            return placed_circuit

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

    os.makedirs(f'{save_path}/{SCHEMES_FOLDER}', exist_ok=True)

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
        meta.add_text("capacitors_num", str(capacitors_num))
        meta.add_text("inductors_num", str(inductors_num))

        if scheme_type == "transient_processes":
            for connection in circuit.layout.values():
                for sub_connection in connection:
                    for sub_sub_connection in sub_connection:
                        if {'type': 'opening_switch'} in sub_sub_connection['elements']:
                            meta.add_text("switch_info", "opening")
                        elif {'type': 'closing_switch'} in sub_sub_connection['elements']:
                            meta.add_text("switch_info", "closing")

        img.save(f'{save_path}/{SCHEMES_FOLDER}/scheme_{index}.png', pnginfo=meta)

        index += 1

    plt.close('all')

    if len(unique_schemes) < 30:
        return {"code": "warning", "message": f'Удалось сгенерировать только {len(unique_schemes)} уникальных схем'}

    return {"code": "success", "message": "Набор схем успешно сгенерирован"}