from src.electric_circuit import ElectricCircuit


circuit = ElectricCircuit(4, 0)

while len(circuit.nodes_coords) < circuit.nodes_num:
    circuit.add_node()

circuit.create_nodes_connections()
circuit.visualise_circuit()

