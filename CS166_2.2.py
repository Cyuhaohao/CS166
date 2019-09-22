
import matplotlib


matplotlib.use('TkAgg')
from pylab import *

n = 100  # size of space: n x n
p = 0.15  # probability of initially panicky individuals


def initialize():
    global config, nextconfig, measurement
    config = zeros([n, n])
    for x in range(n):
        for y in range(n):
            config[x, y] = 1 if random() < p else 0
    nextconfig = zeros([n, n])
    measurement=[]


def observe():
    global config, nextconfig
    cla()
    imshow(config, vmin=0, vmax=1, cmap=cm.binary)
    measurement.append(float(count(config)/10000))


def update():
    global config, nextconfig
    for x in range(n):
        for y in range(n):
            count = 0
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    count += config[(x + dx) % n, (y + dy) % n]
            nextconfig[x, y] = 1 if count >= 4 else 0
    config, nextconfig = nextconfig, config


def count(ar):
    k=0
    for a in ar:
        for b in a:
            if b==1:
                k+=1
    return k


from CS166 import pycxsimulator
import matplotlib.pyplot as plt

pycxsimulator.GUI().start(func=[initialize, observe, update])


plt.plot(measurement)
plt.title("Density Change as Density is 0.15")
plt.xlabel("Number of steps")
plt.ylabel("Density")
plt.savefig("d=0.15.png")
plt.show()
