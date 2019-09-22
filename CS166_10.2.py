import scipy
import matplotlib.pyplot as plt
import numpy as np
import random


resultlist=[]
blist=[]
for b in range(1,31):
    a = []
    for i in range(10000):
        bus=scipy.random.exponential(float(b/10))
        pas=random.uniform(0,bus)
        a.append(bus-pas)
    resultlist.append(np.mean(a))
    blist.append(float(b/10))

plt.plot(blist,resultlist,linewidth="3",alpha=0.8)
plt.plot([0,3],[0,1.5],c="red")
plt.show()


resultlist=[]
blist=[]
for b in range(1,31):
    a = []
    for i in range(10000):
        bus=random.uniform(0,2*float(b/10))
        pas=random.uniform(0,bus)
        a.append(bus-pas)
    resultlist.append(np.mean(a))
    blist.append(float(b/10))

plt.plot(blist,resultlist,linewidth="3",alpha=0.8)
plt.plot([0,3],[0,1.5],c="red")
plt.show()