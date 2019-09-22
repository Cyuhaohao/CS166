import random
import matplotlib.pyplot as plt

#Exercise 2
class Exercise2_1():
    def __init__(self,times):
        self.histlist=[0]*105
        self.histlist[4]=1
        self.times=times
        self.nextlist=[]

    def update(self):
        for i in range(self.times):
            self.nextlist=[0]*105
            for k in range(105):
                if k==0:
                    self.nextlist[1]=self.histlist[0]
                elif k==104:
                    self.nextlist[k-1]+=self.histlist[k]/2
                else:
                    self.nextlist[k + 1] += self.histlist[k] / 2
                    self.nextlist[k - 1] += self.histlist[k] / 2
            self.histlist=self.nextlist

    def draw(self):
        self.update()
        plt.bar(range(-4,101),self.histlist,label="Steps: %i" % self.times)


# simulation1=Exercise2_1(1001)
# simulation1.draw()
# simulation2=Exercise2_1(1000)
# simulation2.draw()
# plt.xlabel("Position")
# plt.ylabel("Probability")
# plt.title("Having left barrier at x=-4")
# plt.legend()
# plt.show()

class Exercise2_2():
    def __init__(self,times):
        self.histlist=[0]*105
        self.histlist[4]=1
        self.times=times
        self.nextlist=[]

    def update(self):
        for i in range(self.times):
            self.nextlist=[0]*105
            for k in range(105):
                if k==0:
                    self.nextlist[1]=self.histlist[0]
                elif k==10:
                    self.nextlist[k+1]+=self.histlist[k]/4
                    self.nextlist[k-1] += 3*self.histlist[k] / 4
                elif k==104:
                    self.nextlist[k-1]+=self.histlist[k]/2
                else:
                    self.nextlist[k + 1] += self.histlist[k] / 2
                    self.nextlist[k - 1] += self.histlist[k] / 2
            self.histlist=self.nextlist
            print(self.histlist)

    def draw(self):
        self.update()
        plt.bar(range(-4, 101), self.histlist, label="Steps: %i" % self.times)

# simulation3=Exercise2_2(1000)
# simulation3.draw()
# simulation4=Exercise2_2(1001)
# simulation4.draw()
# plt.xlabel("Position")
# plt.ylabel("Probability")
# plt.title("Having left barrier at x=-4 and right barrier at x=6")
# plt.legend()
# plt.show()


#Exercise 4
import turtle
import numpy as np
import time
o=0.5

def samplewalk(steps):
    turtle.reset()
    turtle.screensize(canvwidth=10, canvheight=10)
    turtle.home()
    turtle.speed("fastest")
    for i in range(steps):
        turtle.right(random.uniform(0,360))
        turtle.forward(10*np.random.normal(0,o**0.5))
    time.sleep(60)

samplewalk(1600)



