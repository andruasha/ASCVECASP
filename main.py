from src.electric_circuit import ElectricCircuit
import time

circuit = ElectricCircuit(5, 9)

while len(circuit.nodes_coords) < circuit.nodes_num:
    circuit.add_node()

circuit.connect_nodes()