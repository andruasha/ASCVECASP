import random
import copy


class ElementsPlacer:

    def __init__(self, circuit_topology, voltage_sources_num, current_sources_num, resistors_num):
        self.layout = {}
        self.voltage_sources_num = voltage_sources_num
        self.current_sources_num = current_sources_num
        self.resistors_num = resistors_num

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

                    if not resistor_exists:
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
                    raise Exception("Невозможно сгенерировать набор валидных схем при данных параметрах")

        return self

    def distribute_elements(self):
        vs_num = copy.deepcopy(self.voltage_sources_num)
        cs_num = copy.deepcopy(self.current_sources_num)
        r_num = copy.deepcopy(self.resistors_num)

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
            ['resistor'] * r_num
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
                conn_name, idx, entry = random.choice(all_connections)
                element_type = remaining_elements.pop()
                entry['elements'].append({'type': element_type})
