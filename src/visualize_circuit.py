import matplotlib.pyplot as plt


class CircuitVisualize:

    def __init__(self, circuit, circuit_topology):
        self.circuit = circuit
        self.circuit_topology = circuit_topology

    def visualize(self):
        plt.figure(figsize=(5, 5))
        plt.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray')
        plt.xticks(range(-13, 14, 1))
        plt.yticks(range(-13, 14, 1))
        plt.xlim(-13, 13)
        plt.ylim(-13, 13)
        plt.axis('equal')

        for node, coords in self.circuit_topology.nodes.items():
            plt.plot(coords['x'], coords['y'], 'ko')

        for connections in self.circuit.layout.values():
            for segment in connections:
                for i in range(len(segment[0]['connection_coords']) - 1):
                    start, end = segment[0]['connection_coords'][i], segment[0]['connection_coords'][i + 1]
                    plt.plot([start['x'], end['x']], [start['y'], end['y']], 'k-')

        plt.show()
