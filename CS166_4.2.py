import random
import numpy
import matplotlib.pyplot as plt


class TrafficSimulation():
    def __init__(self,length,density,maxvelocity,probslow,steps,times):
        self.length=length
        self.density=density
        self.maxvelocity=maxvelocity
        self.probslow=probslow
        self.current_state= [-1] * self.length
        self.next_state=[-1] * self.length
        self.flowcount=0
        self.steps=steps
        self.times=times

    def initialize(self):
        self.current_state=[-1]*self.length
        num_of_cars=round(self.length*self.density)
        carlist=random.sample(range(self.length),num_of_cars)
        for i in carlist:
            self.current_state[i]=0
        self.next_state=[-1]*self.length
        self.flowcount=0

    def update(self):
        for i in range(len(self.current_state)):
            if self.current_state[i]!=-1:
                empty=self.checkspace(i)
                if empty>self.current_state[i]:
                    self.current_state[i]+=1
                elif empty<self.current_state[i]:
                    self.current_state[i]=empty
                if self.current_state[i]>0:
                    if random.random()<self.probslow:
                        self.current_state[i]-=1
        for i in range(len(self.current_state)):
            speed=self.current_state[i]
            if speed != -1:
                self.next_state[(i+speed)%self.length]=speed
                if (i+speed)%self.length != i+speed:
                    self.flowcount += 1
        self.current_state=self.next_state
        self.next_state=[-1]*self.length

    def checkspace(self,i):
        empty=0
        for a in range(1,self.maxvelocity+1):
            if self.current_state[(i+a)%self.length]==-1:
                empty+=1
            else:
                break
        return empty

    def display(self):
        print(''.join('.' if x==-1 else str(x) for x in self.current_state))

    def simulate(self):
        self.initialize()
        self.display()
        for i in range(self.steps):
            self.update()
            self.display()

    def flow_analysis(self):
        flowcounts=[]
        for time in range(self.times):
            self.initialize()
            for step in range(self.steps):
                self.update()
                if step==99:
                    self.flowcount=0
            flowcounts.append(float(self.flowcount/(self.steps-100)))
        return flowcounts


flowrate_list1=[]
flowrate_list2=[]
density_list1=[]
density_list2=[]

for den in range(1,101):
    density=float(den/100)
    Simulator=TrafficSimulation(length=100,density=density,maxvelocity=5,probslow=0.5,steps=300,times=20)
    flowcounts=Simulator.flow_analysis()
    flowrate_list1.append(numpy.mean(flowcounts))
    density_list1.append(density)
    flowrate_list2.append(flowcounts)
    for i in range(len(flowcounts)):
        density_list2.append(density)


plt.plot(density_list1,flowrate_list1,c="red")
plt.xlabel("Density [cars per site]")
plt.ylabel("Flow [cars per time step]")
plt.title("Simulation")
plt.scatter(density_list2,flowrate_list2,s=3)
plt.show()



