import random


class ElementsPlacer:

    def __init__(self, circuit_topology, voltage_sources_num, current_sources_num, resistors_num, inductances_num,
                 capacities_num):
        self.layout = {}
        self.voltage_sources_num = voltage_sources_num
        self.current_sources_num = current_sources_num
        self.resistors_num = resistors_num
        self.inductances_num = inductances_num
        self.capacities_num = capacities_num

        all_subconnections = []  # список всех ветвей

        # Инициализируем layout и собираем все ветви
        for connection_name, connection_coords in circuit_topology.nodes_connections.items():
            self.layout[connection_name] = []
            for sub_connection in connection_coords:
                entry = {'connection_coords': sub_connection, 'elements': []}
                self.layout[connection_name].append([entry])
                all_subconnections.append((connection_name, len(self.layout[connection_name]) - 1))  # (имя соединения, индекс)

        # Функция для случайного распределения элементов
        def distribute_elements(element_type, count):
            if count == 0:
                return
            chosen_subconnections = random.choices(all_subconnections, k=count)
            for conn_name, idx in chosen_subconnections:
                self.layout[conn_name][idx][0]['elements'].append({'type': element_type})

        # Распределяем все типы элементов
        distribute_elements('resistor', self.resistors_num)
        distribute_elements('inductance', self.inductances_num)
        distribute_elements('capacity', self.capacities_num)
        distribute_elements('voltage_source', self.voltage_sources_num)
        distribute_elements('current_source', self.current_sources_num)
