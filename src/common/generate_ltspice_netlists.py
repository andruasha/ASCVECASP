

def generate_ltpsice_netlist(save_path, circuit, elements_values):
    auxiliary_node_idx = 5
    netlist_lines = []

    for connection_name, branches in circuit.layout.items():
        node_start = connection_name.split("->")[0]
        node_end = connection_name.split("->")[1]

        for branch in branches:
            for index, element in enumerate(branch[0]['elements']):
                if index == 0:
                    netlist_lines.append('')


