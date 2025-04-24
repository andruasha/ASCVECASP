

def generate_ltpsice_netlist(save_path, circuit, elements_values):
    auxiliary_node_idx = 5
    netlist_lines = []

    voltage_source_idx = 1
    current_source_idx = 1
    resistor_idx = 1
    capacitor_idx = 1
    inductor_idx = 1

    for connection_name, branches in circuit.layout.items():
        node_start = int(connection_name.split("->")[0].replace('node', ''))
        node_end = int(connection_name.split("->")[1].replace('node', ''))

        for branch in branches:
            if 'elements' in branch[0].keys():

                for index, element in enumerate(branch[0]['elements']):
                    if index == 0:
                        if len(branch[0]['elements']) == 1:
                            if element['type'] == 'voltage_source':
                                netlist_lines.append(
                                    f"V{voltage_source_idx} N{node_start:03} N{node_end:03} {elements_values['V' + str(voltage_source_idx)]}"
                                )
                                voltage_source_idx += 1

                            elif element['type'] == 'current_source':
                                netlist_lines.append(
                                    f"I{current_source_idx} N{node_start:03} N{node_end:03} {elements_values['I' + str(current_source_idx)]}"
                                )
                                current_source_idx += 1

                            elif element['type'] == 'resistor':
                                netlist_lines.append(
                                    f"R{resistor_idx} N{node_start:03} N{node_end:03} {elements_values['R' + str(resistor_idx)]}"
                                )
                                resistor_idx += 1

                            elif element['type'] == 'capacitor':
                                netlist_lines.append(
                                    f"C{capacitor_idx} N{node_start:03} N{node_end:03} {elements_values['C' + str(capacitor_idx)]}"
                                )
                                capacitor_idx += 1

                            elif element['type'] == 'inductor':
                                netlist_lines.append(
                                    f"L{inductor_idx} N{node_start:03} N{node_end:03} {elements_values['L' + str(inductor_idx)]}"
                                )
                                inductor_idx += 1

                            elif element['type'] == 'active_dipole':
                                netlist_lines.append(
                                    f"ACTIVEDIPOLE N{node_start:03} N{node_end:03} ACTIVEDIPOLE"
                                )

                            elif element['type'] == 'opening_switch':
                                netlist_lines.append(
                                    f"OPENINGSWITCH N{node_start:03} N{node_end:03} OPENINGSWITCH"
                                )

                            elif element['type'] == 'closing_switch':
                                netlist_lines.append(
                                    f"CLOSINGSWITCH N{node_start:03} N{node_end:03} CLOSINGSWITCH"
                                )

                        else:
                            if element['type'] == 'voltage_source':
                                netlist_lines.append(
                                    f"V{voltage_source_idx} N{node_start:03} N{auxiliary_node_idx:03} {elements_values['V' + str(voltage_source_idx)]}"
                                )
                                voltage_source_idx += 1

                            elif element['type'] == 'current_source':
                                netlist_lines.append(
                                    f"I{current_source_idx} N{node_start:03} N{auxiliary_node_idx:03} {elements_values['I' + str(current_source_idx)]}"
                                )
                                current_source_idx += 1

                            elif element['type'] == 'resistor':
                                netlist_lines.append(
                                    f"R{resistor_idx} N{node_start:03} N{auxiliary_node_idx:03} {elements_values['R' + str(resistor_idx)]}"
                                )
                                resistor_idx += 1

                            elif element['type'] == 'capacitor':
                                netlist_lines.append(
                                    f"C{capacitor_idx} N{node_start:03} N{auxiliary_node_idx:03} {elements_values['C' + str(capacitor_idx)]}"
                                )
                                capacitor_idx += 1

                            elif element['type'] == 'inductor':
                                netlist_lines.append(
                                    f"L{inductor_idx} N{node_start:03} N{auxiliary_node_idx:03} {elements_values['L' + str(inductor_idx)]}"
                                )
                                inductor_idx += 1

                            elif element['type'] == 'active_dipole':
                                netlist_lines.append(
                                    f"ACTIVEDIPOLE N{node_start:03} N{auxiliary_node_idx:03} ACTIVEDIPOLE"
                                )

                            elif element['type'] == 'opening_switch':
                                netlist_lines.append(
                                    f"OPENINGSWITCH N{node_start:03} N{auxiliary_node_idx:03} OPENINGSWITCH"
                                )

                            elif element['type'] == 'closing_switch':
                                netlist_lines.append(
                                    f"CLOSINGSWITCH N{node_start:03} N{auxiliary_node_idx:03} CLOSINGSWITCH"
                                )

                            auxiliary_node_idx += 1

                    elif index == len(branch[0]['elements']) - 1:
                        if element['type'] == 'voltage_source':
                            netlist_lines.append(
                                f"V{voltage_source_idx} N{auxiliary_node_idx:03} N{node_end:03} {elements_values['V' + str(voltage_source_idx)]}"
                            )
                            voltage_source_idx += 1

                        elif element['type'] == 'current_source':
                            netlist_lines.append(
                                f"I{current_source_idx} N{auxiliary_node_idx:03} N{node_end:03} {elements_values['I' + str(current_source_idx)]}"
                            )
                            current_source_idx += 1

                        elif element['type'] == 'resistor':
                            netlist_lines.append(
                                f"R{resistor_idx} N{auxiliary_node_idx:03} N{node_end:03} {elements_values['R' + str(resistor_idx)]}"
                            )
                            resistor_idx += 1

                        elif element['type'] == 'capacitor':
                            netlist_lines.append(
                                f"C{capacitor_idx} N{auxiliary_node_idx:03} N{node_end:03} {elements_values['C' + str(capacitor_idx)]}"
                            )
                            capacitor_idx += 1

                        elif element['type'] == 'inductor':
                            netlist_lines.append(
                                f"L{inductor_idx} N{auxiliary_node_idx:03} N{node_end:03} {elements_values['L' + str(inductor_idx)]}"
                            )
                            inductor_idx += 1

                        elif element['type'] == 'active_dipole':
                            netlist_lines.append(
                                f"ACTIVEDIPOLE N{auxiliary_node_idx:03} N{node_end:03} ACTIVEDIPOLE"
                            )

                        elif element['type'] == 'opening_switch':
                            netlist_lines.append(
                                f"OPENINGSWITCH N{auxiliary_node_idx:03} N{node_end:03} OPENINGSWITCH"
                            )

                        elif element['type'] == 'closing_switch':
                            netlist_lines.append(
                                f"CLOSINGSWITCH N{auxiliary_node_idx:03} N{node_end:03} CLOSINGSWITCH"
                            )

                        auxiliary_node_idx += 1

                    else:
                        if element['type'] == 'voltage_source':
                            netlist_lines.append(
                                f"V{voltage_source_idx} N{auxiliary_node_idx:03} N{auxiliary_node_idx+1:03} {elements_values['V' + str(voltage_source_idx)]}"
                            )
                            voltage_source_idx += 1

                        elif element['type'] == 'current_source':
                            netlist_lines.append(
                                f"I{current_source_idx} N{auxiliary_node_idx:03} N{auxiliary_node_idx+1:03} {elements_values['I' + str(current_source_idx)]}"
                            )
                            current_source_idx += 1

                        elif element['type'] == 'resistor':
                            netlist_lines.append(
                                f"R{resistor_idx} N{auxiliary_node_idx:03} N{auxiliary_node_idx+1:03} {elements_values['R' + str(resistor_idx)]}"
                            )
                            resistor_idx += 1

                        elif element['type'] == 'capacitor':
                            netlist_lines.append(
                                f"C{capacitor_idx} N{auxiliary_node_idx:03} N{auxiliary_node_idx+1:03} {elements_values['C' + str(capacitor_idx)]}"
                            )
                            capacitor_idx += 1

                        elif element['type'] == 'inductor':
                            netlist_lines.append(
                                f"L{inductor_idx} N{auxiliary_node_idx:03} N{auxiliary_node_idx+1:03} {elements_values['L' + str(inductor_idx)]}"
                            )
                            inductor_idx += 1

                        elif element['type'] == 'active_dipole':
                            netlist_lines.append(
                                f"ACTIVEDIPOLE N{auxiliary_node_idx:03} N{auxiliary_node_idx+1:03} ACTIVEDIPOLE"
                            )

                        elif element['type'] == 'opening_switch':
                            netlist_lines.append(
                                f"OPENINGSWITCH N{auxiliary_node_idx:03} N{auxiliary_node_idx+1:03} OPENINGSWITCH"
                            )

                        elif element['type'] == 'closing_switch':
                            netlist_lines.append(
                                f"CLOSINGSWITCH N{auxiliary_node_idx:03} N{auxiliary_node_idx+1:03} CLOSINGSWITCH"
                            )

                        auxiliary_node_idx += 1

    with open(save_path, 'w', encoding='utf-8') as file:
        for line in netlist_lines:
            file.write(line + '\n')

