class ElementsPlacer:

    def __init__(self, circuit_topology, voltage_sources_num, current_sources_num, resistors_num, inductances_num, capacities_num):
        self.layout = {}
        self.voltage_sources_num = voltage_sources_num
        self.current_sources_num = current_sources_num
        self.resistors_num = resistors_num
        self.inductances_num = inductances_num
        self.capacities_num = capacities_num

        for connection_name, connection_coords in circuit_topology.nodes_connections.items():
            self.layout[connection_name] = []
            for sub_connection in connection_coords:
                self.layout[connection_name].append([{'connection_coords': sub_connection, 'elements': []}])
