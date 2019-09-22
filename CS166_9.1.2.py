import networkx as nx

nodes = 1000
degree = 40

networks = {'erdos_renyi': nx.erdos_renyi_graph(nodes, degree / (nodes - 1)),
            'watts_strogatz': nx.watts_strogatz_graph(nodes, degree, 1),  # probability of rewiring each edge
            'barabasi_albert': nx.barabasi_albert_graph(nodes, degree // 2)
            # Number of edges to attach from a new node to existing nodes
            }

for key, g in networks.items():
    print(key)
    print(g.number_of_nodes(), 'nodes and', g.number_of_edges(), 'edges')
    print('Average degree:', sum(g.degree[n] for n in g.nodes) / g.number_of_nodes())
    print('Average degree with built-in method: ', round(sum(list(zip(*g.degree()))[1]) / g.number_of_nodes(), 2))
    print('Average neighbor degree:', sum(g.degree[a] + g.degree[b] for a, b in g.edges) / g.number_of_edges() / 2)
    print('Average neighbor degree with built-in method: ',
          round((sum(nx.average_neighbor_degree(g).values())) / g.number_of_nodes(), 2))
    print('')
