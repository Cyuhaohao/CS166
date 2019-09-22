import matplotlib
matplotlib.use('TkAgg')
from pylab import *
import networkx as nx
import random as rd

def initialize():
    global g
    g = nx.karate_club_graph()
    g.pos = nx.spring_layout(g)
    for i in g.nodes:
        g.nodes[i]['state'] = 1 if random() < .5 else 0

def observe():
    global g
    nx.draw(g, vmin = 0, vmax = 1,
            node_color = [g.nodes[i]['state'] for i in g.nodes],
            pos = g.pos)


# Normal
def update():
    global g
    listener = rd.choice(list(g.nodes))
    speaker = rd.choice(list(g.neighbors(listener)))
    g.nodes[listener]['state'] = g.nodes[speaker]['state']


# Reverse
def update():
    global g
    speaker = rd.choice(list(g.nodes))
    listener = rd.choice(list(g.neighbors(speaker)))
    g.nodes[listener]['state'] = g.nodes[speaker]['state']


# Edge-based
def update():
    global g
    edges = rd.choice(list(g.edges))
    listener = rd.choice(edges)
    for i in edges:
        if listener!=i:
            speaker=i
    g.nodes[listener]['state'] = g.nodes[speaker]['state']


def ifstop():
    vote=g.nodes[0]['state']
    for i in g.nodes:
        if g.nodes[i]['state']!=vote:
            return False
    return True


num=[]
x=[]
for i in range(200):
    initialize()
    k=0
    while not ifstop():
        update()
        k+=1
    num.append(k)
    x.append(i)



plt.scatter(x,num)
plt.hlines(mean(num),xmin=1,xmax=200,color="red")
plt.text(-5, 1800, "The average time is %f steps" % mean(num),size=18)
plt.title("Time of steps to consensus(Edge-based)")
plt.xlabel("Number of trials")
plt.ylabel("Time of steps")
plt.show()


