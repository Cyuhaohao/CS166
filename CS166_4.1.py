import random


class TrafficSimulation():
    def __init__(self,length,density,maxvelocity,probslow):
        self.length=length
        self.density=density
        self.maxvelocity=maxvelocity
        self.probslow=probslow
        self.current_state= [-1] * 100
        self.next_state=[-1]*100


    def initialize(self):
        num_of_cars=round(self.length*self.density)
        carlist=random.sample(range(100),num_of_cars)
        for i in carlist:
            self.current_state[i]=0
        print(self.current_state)

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
                self.next_state[i - speed]=speed
        self.current_state=self.next_state
        self.next_state=[-1]*100

    def checkspace(self,i):
        empty=0
        for a in range(1,self.maxvelocity+1):
            if self.current_state[i - a]==-1:
                empty+=1
            else:
                break
        return empty

    def display(self):
        print(''.join('.' if x==-1 else str(x) for x in self.current_state))

    def simulate(self):
        self.initialize()
        self.display()
        for i in range(150):
            self.update()
            self.display()


Simulator1=TrafficSimulation(length=100,density=0.03,maxvelocity=5,probslow=0.5)
Simulator2=TrafficSimulation(length=100,density=0.1,maxvelocity=5,probslow=0.5)
Simulator2.simulate()
