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
