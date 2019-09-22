from matplotlib import pyplot as plt
import networkx as nx
import random
import numpy as np


class SocialDynamicsSimulation:
    '''
    Simulate social dynamics by strengthening opinions and connection weights
    based on random interactions between nodes.
    '''

    def __init__(self, network_size=50, alpha=0.03, beta=0.3, gamma=8):
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
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

    # def alpha_generate(self):
    #     alpha_index=random.random()
    #     if alpha_index<float(1/6):
    #         return alpha
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
        #self.graph = nx.barabasi_albert_graph(50, 1)
        for edge in self.graph.edges:
            self.graph.edges[edge]['weight'] = 0.5
        for node in self.graph.nodes:
            self.graph.nodes[node]['opinion1'] = random.randint(0, 1)
            self.graph.nodes[node]['opinion2'] = random.randint(0, 1)
            # self.graph.nodes[node]['alpha'] = self.alpha_generate()
            # self.graph.nodes[node]['beta'] = self.beta_generate()
            # self.graph.nodes[node]['gamma'] = self.gamma_genrate()
        self.layout = nx.spring_layout(self.graph)  # Initial visual layout
        self.step = 0

    def observe(self):
        '''
        Draw the state of the network.
        '''
        self.layout = nx.spring_layout(self.graph, pos=self.layout, iterations=5)
        plt.clf()
        plt.subplot(121)
        nx.draw(
            self.graph, pos=self.layout, with_labels=True,
            node_color=[self.graph.nodes[i]['opinion1'] for i in self.graph.nodes],
            edge_color=[self.graph.edges[i, j]['weight'] for i, j in self.graph.edges],
            edge_cmap=plt.cm.binary, edge_vmin=0, edge_vmax=1,
            alpha=0.7, vmin=0, vmax=1)
        plt.subplot(122)
        nx.draw(
            self.graph, pos=self.layout, with_labels=True,
            node_color=[self.graph.nodes[i]['opinion2'] for i in self.graph.nodes],
            edge_color=[self.graph.edges[i, j]['weight'] for i, j in self.graph.edges],
            edge_cmap=plt.cm.binary, edge_vmin=0, edge_vmax=1,
            alpha=0.7, vmin=0, vmax=1)
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
            # alphas = [self.graph.nodes[n]['alpha'] for n in edge]
            # betas = [self.graph.nodes[n]['beta'] for n in edge]
            # gammas = [self.graph.nodes[n]['gamma'] for n in edge]

            for i in [0, 1]:
                self.graph.nodes[edge[i]]['opinion1'] = (
                        opinions_1[i] + self.alpha * weight * (opinions_1[1 - i] - opinions_1[i]))
                self.graph.nodes[edge[i]]['opinion2'] = (
                        opinions_2[i] + self.alpha * weight * (opinions_2[1 - i] - opinions_2[i]))

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
print([sim.graph.edges[i, j]['weight'] for i, j in sim.graph.edges])
for i in range(10):
    for i in range(4000):
        sim.update()
    sim.observe()
print([sim.graph.nodes[i]['opinion1'] for i in sim.graph.nodes])
