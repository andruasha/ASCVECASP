from src.electric_circuit import ElectricCircuit
import time

circuit = ElectricCircuit(8, 9)

while len(circuit.nodes_coords) < circuit.nodes_num:
    circuit.add_node()

circuit.connect_nodes()

print(circuit.get_num_branches())
