import random
import io
import os
import matplotlib.pyplot as plt
from PIL import Image, PngImagePlugin
from conf.config import SCALE
from conf.config import IMAGES_FOLDER
from conf.config import SPICE_FOLDER
from src.common.compare_functions import is_topologies_equal, is_layouts_equal
from src.common.electric_circuit import ElectricCircuit
from src.common.elements_places import ElementsPlacer
from src.common.visualize_circuit import CircuitVisualize
from src.common.generate_ltspice_netlists import generate_ltpsice_netlist


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
            if all(not is_topologies_equal(topo, u) for u in unique):
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
            if is_topologies_equal(topology_1, existing_topology):
                if is_layouts_equal(circuit_1.layout, existing_circuit.layout):
                    is_unique = False
                    break

        if is_unique:
            unique_schemes.append((topology_1, circuit_1))

    os.makedirs(f'{save_path}/{IMAGES_FOLDER}', exist_ok=True)
    os.makedirs(f'{save_path}/{SPICE_FOLDER}', exist_ok=True)

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

        elements_values = {}

        for i in range(voltage_sources_num):
            elements_values[f"V{i+1}"] = str(random.randint(15, 310))
        for i in range(current_sources_num):
            elements_values[f"I{i+1}"] = str(round(random.uniform(0.15, 3), 2))
        for i in range(resistors_num):
            elements_values[f"R{i+1}"] = str(random.randint(5, 100))
        for i in range(capacitors_num):
            elements_values[f"C{i+1}"] = str(round(random.uniform(0.05, 1), 2))
        for i in range(inductors_num):
            elements_values[f"L{i+1}"] = str(random.randint(1, 20))

        meta = PngImagePlugin.PngInfo()

        for element_name, element_value in elements_values.items():
            if element_name.startswith("V"):
                meta.add_text(element_name, f"{element_value} В")
            elif element_name.startswith("I"):
                meta.add_text(element_name, f"{element_value} А")
            elif element_name.startswith("R"):
                meta.add_text(element_name, f"{element_value} Ом")
            elif element_name.startswith("C"):
                meta.add_text(element_name, f"{element_value} мкФ")
            elif element_name.startswith("L"):
                meta.add_text(element_name, f"{element_value} мГн")

        if scheme_type == "transient_processes":
            for connection in circuit.layout.values():
                for sub_connection in connection:
                    for sub_sub_connection in sub_connection:
                        if {'type': 'opening_switch'} in sub_sub_connection['elements']:
                            meta.add_text("switch_info", "opening")
                        elif {'type': 'closing_switch'} in sub_sub_connection['elements']:
                            meta.add_text("switch_info", "closing")

        img.save(f'{save_path}/{IMAGES_FOLDER}/scheme_{index}.png', pnginfo=meta)

        generate_ltpsice_netlist(
            save_path=f'{save_path}/{SPICE_FOLDER}/scheme_{index}.net',
            circuit_layout=circuit.layout,
            elements_values=elements_values
        )

        index += 1

    plt.close('all')

    if len(unique_schemes) < 30:
        return {"code": "warning", "message": f'Удалось сгенерировать только {len(unique_schemes)} уникальных схем'}

    return {"code": "success", "message": "Набор схем успешно сгенерирован"}