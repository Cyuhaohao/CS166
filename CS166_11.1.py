import matplotlib
matplotlib.use('TkAgg')
from pylab import *
import random
import scipy
import pylab as plt

n = 100  # size of space: n x n
p = 0.5  # probability of initially panicky individuals
T = 1
J = 6.34369e-21  # Interaction constant for iron [Joule]
kB = 1.38065e-23  # Boltzmann constant [Joule / Kelvin]


def initialize():
    global config
    config = zeros([n, n])
    for x in range(n):
        for y in range(n):
            if random.random() < p:
                config[x, y] = 1
            else:
                config[x, y] = -1


def observe():
    global config
    cla()
    imshow(config, vmin=0, vmax=1, cmap=cm.binary)


def update():
    global config
    for i in range(1000):
        i = random.randint(0,n-1)
        j = random.randint(0,n-1)
        E = 2*J*(config[i,j]*config[i-1,j] + config[i,j]*config[i,j-1] +
            config[i,j]*config[i,(j+1)%n] + config[i,j]*config[(i+1)%n,j])
        log_p = -E / (T * kB)
        if scipy.log(scipy.random.uniform(0, 1)) < log_p:
            config[i,j] = -config[i,j]




from CS166 import pycxsimulator
pycxsimulator.GUI().start(func=[initialize, observe, update])

# list=[]
# for i in range(100):
#     black=0
#     initialize()
#     update()
#     for l in range(n):
#         for m in range(n):
#             if config[l,m]==-1:
#                 black += 1
#     list.append(float(black/(n*n)))
#     print(i)
#
# plt.hist(list)
# plt.show()

