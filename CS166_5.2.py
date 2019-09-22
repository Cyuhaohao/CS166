import networkx as nx
import matplotlib.pyplot as plt

# creating a new empty Graph object
#g = nx.Graph()
#f = nx.Graph()

# adding a node named 'John'
#g.add_node('John')


#g.add_nodes_from(['Josh', 'Jane', 'Jess', 'Jack'])

k=nx.wheel_graph(100)

nx.draw(k,node_size=50)
plt.show()