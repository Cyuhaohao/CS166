from matplotlib import pyplot as plt
import networkx as nx
import random
import numpy as np


class SocialDynamicsSimulation:
    '''
    Simulate social dynamics by strengthening opinions and connection weights
    based on random interactions between nodes.
    '''

    def __init__(self, network_size=50):
        '''
        Inputs:

            network_size (int) The number of nodes in the random Watts-Strogatz
              small-world network. Default: 50.

            alpha (float) The rate at which nodes adjust their opinions to
              match neighboring nodes' opinions during interactions.
              Default: 0.03.

            beta (float) The rate at which edge weights are changed in
              response to differing opinions. Default: 0.3.

            gamma (float) The pickiness of nodes. Nodes with opinions differing
              by more than 1/gamma will result in an edge weight decreasing.
              Default: 4.
        '''
        self.network_size = network_size
        self.beta = 0.3
        self.gamma = 8

    def alpha_generate(self):
        alpha_index=random.random()
        if alpha_index<float(1/5):
            return 0
        elif alpha_index>float(4/5):
            return 0.5
        else:
            return 0.03


    def find_color(self,i):
        if self.graph.nodes[i]['alpha'] == 0:
            return "red"
        if self.graph.nodes[i]['alpha'] == 0.03:
            return "green"
        if self.graph.nodes[i]['alpha'] == 0.5:
            return "blue"

    #
    # def beta_generate(self):
    #     beta = np.random.normal(0.25,0.15,1)
    #     if beta < 0:
    #         beta=0
    #     if beta>1:
    #         beta=1
    #     return beta
    #
    # def gamma_genrate(self):
    #     gamma = np.random.normal(4,1.3,1)
    #     if gamma<0.5:
    #         gamma=0.5
    #     if gamma>7.5:
    #         gamma=7.5
    #     return gamma

    def initialize(self):
        '''
        Initialize the simulation with a random graph, with random 0 or 1
        opinions assigned to all nodes and initial edge weights of 0.5.
        '''
        self.graph = nx.watts_strogatz_graph(50, 5, 0.5)
        for edge in self.graph.edges:
            self.graph.edges[edge]['weight'] = 0.5
        for node in self.graph.nodes:
            self.graph.nodes[node]['opinion1'] = random.randint(0, 1)
            self.graph.nodes[node]['opinion2'] = random.randint(0, 1)
            self.graph.nodes[node]['alpha'] = self.alpha_generate()

        self.layout = nx.spring_layout(self.graph)  # Initial visual layout
        self.step = 0

    def observe(self):
        '''
        Draw the state of the network.
        '''
        self.layout = nx.spring_layout(self.graph, pos=self.layout, iterations=5)
        plt.clf()
        plt.subplot(131)
        nx.draw(
            self.graph, pos=self.layout, with_labels=False,
            node_color=[self.graph.nodes[i]['opinion1'] for i in self.graph.nodes],
            edge_color=[self.graph.edges[i, j]['weight'] for i, j in self.graph.edges],
            node_size=100,
            edge_cmap=plt.cm.binary, edge_vmin=0, edge_vmax=1,
            alpha=0.7, vmin=0, vmax=1)
        plt.subplot(132)
        nx.draw(
            self.graph, pos=self.layout, with_labels=True,
            node_color=[self.graph.nodes[i]['opinion2'] for i in self.graph.nodes],
            edge_color=[self.graph.edges[i, j]['weight'] for i, j in self.graph.edges],
            edge_cmap=plt.cm.binary, edge_vmin=0, edge_vmax=1,
            alpha=0.7, vmin=0, vmax=1)
        plt.subplot(133)
        nx.draw(
            self.graph, pos=self.layout, with_labels=True,
            node_color=[self.find_color(i) for i in self.graph.nodes],
            edge_color=[self.graph.edges[i, j]['weight'] for i, j in self.graph.edges],
            edge_cmap=plt.cm.binary, edge_vmin=0, edge_vmax=1,
            alpha=0.4, vmin=0, vmax=1)
        plt.show()
        plt.title('Step: ' + str(self.step))

    def update(self):
        if random.uniform(0, 1) < 0.01:
            # Create a new edge with weight 0.5 between two unconnected nodes
            nodes = list(self.graph.nodes)
            while True:
                new_edge = random.sample(nodes, 2)
                if new_edge not in self.graph.edges:
                    break
            self.graph.add_edge(new_edge[0], new_edge[1], weight=0.5)
        else:
            # Select a random edge and update node opinions and edge weight
            edge = random.choice(list(self.graph.edges))
            weight = self.graph.edges[edge]['weight']
            opinions_1 = [self.graph.nodes[n]['opinion1'] for n in edge]
            opinions_2 = [self.graph.nodes[n]['opinion2'] for n in edge]
            alphas = [self.graph.nodes[n]['alpha'] for n in edge]

            for i in [0, 1]:
                self.graph.nodes[edge[i]]['opinion1'] = (
                        opinions_1[i] + float(alphas[i]) * weight * (opinions_1[1 - i] - opinions_1[i]))
                self.graph.nodes[edge[i]]['opinion2'] = (
                        opinions_2[i] + float(alphas[i]) * weight * (opinions_2[1 - i] - opinions_2[i]))

            self.graph.edges[edge]['weight'] = (
                    weight +
                    self.beta * weight * (1 - weight) *
                    (1 - self.gamma * abs(opinions_1[0] - opinions_1[1]))
                    +(self.beta * weight * (1 - weight) *
                    (1 - self.gamma * abs(opinions_2[0] - opinions_2[1]))))

            # Remove very weak connections
            if self.graph.edges[edge]['weight'] < 0.05:
                self.graph.remove_edge(*edge)
        self.step += 1



sim = SocialDynamicsSimulation()
sim.initialize()
plt.figure()
sim.observe()
for i in range(10):
    for i in range(5000):
        sim.update()
    sim.observe()
print([sim.graph.nodes[i]['opinion1'] for i in sim.graph.nodes])
print([sim.graph.nodes[i]['opinion2'] for i in sim.graph.nodes])
print(np.std([sim.graph.nodes[i]['opinion1'] for i in sim.graph.nodes],ddof=1))
print(np.std([sim.graph.nodes[i]['opinion2'] for i in sim.graph.nodes],ddof=1))