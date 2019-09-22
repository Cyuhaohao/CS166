import networkx as nx
import pylab as plt
import numpy as np

alpha=0.85
n=30

g = nx.erdos_renyi_graph(n, 0.05, directed=True, seed=123)
nx.draw(g, pos=nx.kamada_kawai_layout(g))
plt.show()
rank_networkx=list(nx.pagerank(g).values())


def simulate(g,iteration, alpha):
    rank = np.zeros(g.number_of_nodes())
    node = np.random.choice(list(g.nodes()))

    for i in range(iteration):
        if np.random.rand() < alpha:
            if len(list(g.neighbors(node))) > 0:
                next_node = np.random.choice(list(g.neighbors(node)))
            else:
                next_node = np.random.choice(list(g.nodes))
            rank[next_node] += 1
            node = next_node
        else:
            next_node = np.random.choice(list(g.nodes))
            rank[next_node] += 1
            node = next_node

    page_rank = rank/np.sum(rank)
    return(page_rank)


diff_result=[]
for iteration in range(0,100000,100):
    diff=[]
    rank_simulation=simulate(g,iteration,alpha)
    for i in range(n):
        diff.append(abs(rank_networkx[i]-rank_simulation[i]))
    diff_result.append(np.mean(diff))

x=range(0,100000,100)

plt.scatter(x,diff_result,s=3)
plt.show()

