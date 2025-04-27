import random
import copy


class ElementsPlacer:

    def __init__(
            self,
            circuit_topology,
            voltage_sources_num,
            current_sources_num,
            resistors_num,
            inductors_num,
            capacitors_num,
            scheme_type
    ):
        self.layout = {}
        self.voltage_sources_num = voltage_sources_num
        self.current_sources_num = current_sources_num
        self.resistors_num = resistors_num
        self.inductors_num = inductors_num
        self.capacitors_num = capacitors_num
        self.scheme_type = scheme_type

        for connection_name, connection_coords in circuit_topology.nodes_connections.items():
            self.layout[connection_name] = []
            for sub_connection in connection_coords:
                entry = {'connection_coords': sub_connection, 'elements': []}
                self.layout[connection_name].append([entry])

    def place_elements(self):
        def is_layout_valid(layout):
            for connection_name, connections in layout.items():
                for connection in connections:
                    if len(connection[0]['elements']) > 8:
                        return False

                voltage_source_exists = False
                connection_with_voltage_source = None
                resistor_exists = False

                for connection in connections:
                    for element_type in connection[0]['elements']:
                        if element_type['type'] == 'voltage_source':
                            voltage_source_exists = True
                            connection_with_voltage_source = connection

                if voltage_source_exists:
                    for connection in connections:
                        if len(connections) == 1:
                            resistor_exists = True
                            continue
                        if connection != connection_with_voltage_source:
                            for element_type in connection[0]['elements']:
                                if element_type['type'] == 'resistor':
                                    resistor_exists = True
                                if self.scheme_type == "active_dipole":
                                    if element_type['type'] == 'active_dipole':
                                        return False

                    if not resistor_exists:
                        return False
                if self.scheme_type == "transient_processes":
                    for connection in connections:
                        elements = connection[0]['elements']
                        types_in_connection = {el['type'] for el in elements}
                        if 'voltage_source' in types_in_connection and 'capacitor' in types_in_connection:
                            capacitor_indices = [i for i, el in enumerate(elements) if el['type'] == 'capacitor']
                            for idx in capacitor_indices:
                                has_resistor = False
                                if idx > 0 and elements[idx - 1]['type'] == 'resistor':
                                    has_resistor = True
                                elif idx < len(elements) - 1 and elements[idx + 1]['type'] == 'resistor':
                                    has_resistor = True
                                if not has_resistor:
                                    return False

                        for i in range(len(elements) - 1):
                            if elements[i]['type'] == 'current_source' and elements[i + 1]['type'] == 'inductor':
                                if i + 2 < len(elements) and elements[i + 2]['type'] == 'resistor':
                                    continue
                                elif i > 0 and elements[i - 1]['type'] == 'resistor':
                                    continue
                                else:
                                    return False
                            elif elements[i]['type'] == 'inductor' and elements[i + 1]['type'] == 'current_source':
                                if i > 0 and elements[i - 1]['type'] == 'resistor':
                                    continue
                                else:
                                    return False

            return True

        backup = copy.deepcopy(self.layout)
        regeneration_count = 0
        max_regenerations = 50000

        while True:
            self.layout = copy.deepcopy(backup)
            self.distribute_elements()

            if is_layout_valid(self.layout):
                break
            else:
                regeneration_count += 1

                if regeneration_count >= max_regenerations:
                    return {"code": "error", "message": "Невозможно сгенерировать валидные схемы при заданных параметрах"}

        return self

    def distribute_elements(self):
        vs_num = copy.deepcopy(self.voltage_sources_num)
        cs_num = copy.deepcopy(self.current_sources_num)
        r_num = copy.deepcopy(self.resistors_num)
        i_num = copy.deepcopy(self.inductors_num)
        c_num = copy.deepcopy(self.capacitors_num)

        all_connections = []

        for conn_name, conn_sublist in self.layout.items():
            for idx, branch in enumerate(conn_sublist):
                for entry in branch:
                    all_connections.append((conn_name, idx, entry))

        while cs_num > 0:
            empty_connections = []
            for conn_name, idx, entry in all_connections:
                if len(entry['elements']) == 0:
                    empty_connections.append((conn_name, idx, entry))

            conn_name, idx, entry = random.choice(empty_connections)
            entry['elements'].append({'type': 'current_source'})
            cs_num -= 1

        while vs_num > 0:
            empty_connections = []
            for conn_name, idx, entry in all_connections:
                if len(entry['elements']) == 0:
                    empty_connections.append((conn_name, idx, entry))

            no_cs_connections = []
            for conn_name, idx, entry in all_connections:
                if len(entry['elements']) != 0:
                    if all(element['type'] != "current_source" for element in entry['elements']):
                        no_cs_connections.append((conn_name, idx, entry))

            if len(empty_connections) >= 1:
                conn_name, idx, entry = random.choice(empty_connections)
                entry['elements'].append({'type': 'voltage_source'})
                vs_num -= 1
            else:
                conn_name, idx, entry = random.choice(no_cs_connections)
                entry['elements'].append({'type': 'voltage_source'})
                vs_num -= 1

        remaining_elements = (
                ['resistor'] * r_num +
                ['inductor'] * i_num +
                ['capacitor'] * c_num +
                (['active_dipole'] if self.scheme_type == 'active_dipole' else []) +
                ([random.choice(['opening_switch', 'closing_switch'])] if self.scheme_type == 'transient_processes' else [])
        )
        random.shuffle(remaining_elements)

        while remaining_elements:
            empty_connections = [(conn_name, idx, entry) for conn_name, idx, entry in all_connections if
                                 not entry['elements']]

            if empty_connections:
                conn_name, idx, entry = random.choice(empty_connections)
                element_type = remaining_elements.pop()
                entry['elements'].append({'type': element_type})

            else:
                available_connections = []
                element_type = remaining_elements.pop()
                for conn_name, idx, entry in all_connections:
                    if all(element['type'] != element_type for element in entry['elements']):
                        available_connections.append((conn_name, idx, entry))

                if available_connections:
                    conn_name, idx, entry = random.choice(available_connections)
                else:
                    conn_name, idx, entry = random.choice(all_connections)

                entry['elements'].append({'type': element_type})
