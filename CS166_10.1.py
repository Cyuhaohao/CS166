import random
import pylab as plt
import numpy as np

ph=0.6
pt=0.4

steplist=[]
xlist=[]


# for i in range(30):
#     if random.random()<0.6:
#         step+=1
#     else:
#         step-=1
#     steplist.append(step)
#
# plt.plot(steplist)
# plt.show()


for i in range(200):
    step = 0
    for k in range(30):
        if random.random() < 0.6:
            step+=1
        else:
            step-=1
    steplist.append(step)
    xlist.append(i)

plt.scatter(xlist,steplist)
print(np.var(steplist))
print(np.mean(steplist))
plt.show()