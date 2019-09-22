

import random as RD
import scipy as SP
import numpy


width = 64
height = 64
empty, tree, fire, char = range(4)
num_of_sim=10
spreadProb=0.5


def init():
    global time, config, nextConfig

    time = []
    config=[]
    nextConfig=[]
    c=SP.zeros([height, width])

    for i in range(num_of_sim):
        time.append(0)
        config.append(SP.zeros([height, width]))
        for x in range(width):
            for y in range(height):
                if RD.random() < initProb:
                    state = tree
                else:
                    state = empty
                config[i][y][x] = state
        config[i][height//2, width//2] = fire
        nextConfig.append(SP.zeros([height, width]))

def step():
    global time, config, nextConfig

    for i in range(num_of_sim):
        if i in stop_list:
            pass
        else:
            time[i] += 1
            for x in range(width):
                for y in range(height):
                    state = config[i][y][x]
                    if state == fire:
                        state = char
                    elif state == tree:
                        for dx in range(-1, 2):
                            for dy in range(-1, 2):
                                if config[i][(y+dy)%height, (x+dx)%width] == fire:
                                    if RD.random() < spreadProb:
                                        state = fire
                                    else:
                                        state = tree
                    nextConfig[i][y][x] = state
            config[i], nextConfig[i] = nextConfig[i], config[i]
            if ifstop(config[i],nextConfig[i]):
                stop_list.append(i)


def count(ar):
    tree=0
    char=0
    for a in ar:
        for b in a:
            if b==1:
                tree+=1
            if b==3:
                char+=1
    return tree,char


def ifstop(m1,m2):
    for w in range(width):
        for h in range(height):
            if m1[h][w]!=m2[h][w]:
                return False
    return True


import matplotlib.pyplot as plt

x=[]
time_list=[]
burnt_area=[]
burnt_percentage=[]
for i in range(5,101,5):
    initProb = float(i/100)
    x.append(initProb)
    stop_list = []
    area=[]
    percentage=[]
    init()
    while len(stop_list)!=num_of_sim:
        step()
    for i in range(num_of_sim):
        area.append(count(config[i])[1])
        percentage.append(float(count(config[i])[1]/(count(config[i])[0]+count(config[i])[1])))
    time_list.append(numpy.mean(time))
    burnt_area.append(numpy.mean(area))
    burnt_percentage.append(numpy.mean(percentage))

plt.plot(x,time_list)
plt.title("Plot of Stop Time")
plt.xlabel("Initial Probability of Tree Area")
plt.ylabel("Average Stop Time")
plt.show()

plt.plot(x,burnt_area)
plt.title("Plot of Number of Burnt Areas")
plt.xlabel("Initial Probability of Tree Area")
plt.ylabel("Average Number of Burnt Areas")
plt.show()

plt.plot(x,burnt_percentage)
plt.title("Plot of Proportion of Burnt Areas")
plt.xlabel("Initial Probability of Tree Area")
plt.ylabel("Average Proportion of Burnt Areas")
plt.show()