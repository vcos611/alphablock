import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

class graph:

    def __init__(self, n_nodes, weights=None):
        self.n_nodes = n_nodes
        if weights is None:
            self.weights = np.zeros((n_nodes, n_nodes))
            self.assign_random_weights()
        else:
            self.weights = weights

    def assign_random_weights(self, network_delay_factor=0.5, seed=None):            
        """
        randomly generated following the log-normal distribution with mean of 0 and variance of 𝛿^2, in which 𝛿 is the network delay factor
        """
        if seed is not None:
            np.random.seed(seed)

        mu = 0  # mean of the log-normal distribution
        sigma = network_delay_factor  # standard deviation of the log-normal distribution

        for i in range(len(self.weights)):
            for j in range(i+1, len(self.weights)):
                if i != j:
                    self.weights[i][j] = round(np.random.lognormal(mu, sigma, 1)[0], 2)
                else:
                    self.weights[i][j] = 0

    def draw(self):
        G = nx.Graph()
        for i in range(self.n_nodes):
            for j in range(i+1, self.n_nodes):
                if self.weights[i][j] > 0:
                    G.add_edge(i, j, weight=self.weights[i][j])
        
        e = [(u, v) for (u, v, d) in G.edges(data=True)]

        pos = nx.spring_layout(G, seed=7)  # positions for all nodes - seed for reproducibility

        # nodes
        nx.draw_networkx_nodes(G, pos, node_size=700)

        # edges
        nx.draw_networkx_edges(G, pos, edgelist=e, width=6)

        # node labels
        nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")
        # edge weight labels
        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, edge_labels)

        ax = plt.gca()
        ax.margins(0.08)
        plt.axis("off")
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    np.random.seed(42)  # Fix the random seed
    g = graph(5)
    g.draw()
