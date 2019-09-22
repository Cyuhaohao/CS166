import random
import matplotlib.pyplot as plt
import numpy as np
from pandas import *


def simulate():
    cash=250
    previous_result=1
    for i in range(20):
        if cash>0:
            strategy=int(cash/16)*previous_result
            if strategy<=cash:
                input=strategy
            else:
                input=cash

            if random.random()<0.6:
                cash+=input
                previous_result=1
            else:
                cash-=input
                previous_result+=1
        else:
            break
    return cash

resultlist=[]
for i in range(100000):
    resultlist.append(simulate())


def simulate2():
    cash = 250
    for i in range(20):
        if cash > 0:
            if random.random() < 0.6:
                cash += int(cash*0.2)
            else:
                cash -= int(cash*0.2)
        else:
            break
    return cash

resultlist2=[]
for i in range(100000):
    resultlist2.append(simulate2())

print(np.mean(resultlist))
print(np.percentile(np.sort(resultlist),2.5))
print(np.percentile(np.sort(resultlist),97.5))
plt.hist(resultlist)
plt.show()

print(np.mean(resultlist2))
print(np.percentile(np.sort(resultlist2),2.5))
print(np.percentile(np.sort(resultlist2),97.5))
plt.hist(resultlist2)
plt.show()