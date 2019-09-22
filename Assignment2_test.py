import random
import numpy
import matplotlib.pyplot as plt
import time
import matplotlib

matplotlib.use('TkAgg')

import pylab as PL
import random as RD
import scipy as SP




class TrafficSimulation():
    def __init__(self,length,density,maxvelocity,probslow,steps,times,lane):
        self.length=length
        self.density=density
        self.maxvelocity=maxvelocity
        self.probslow=probslow
        self.flowcount=0
        self.steps=steps
        self.times=times
        self.lane=lane
        self.current_state=self.array_generate()
        self.next_state=self.array_generate()

    def array_generate(self):
        l = numpy.zeros([self.lane, self.length])
        for a in range(self.lane):
            for b in range(self.length):
                l[a][b] = -1
        return l

    def initialize(self):
        self.current_state=self.array_generate()
        num_of_cars=round(self.length*self.lane*self.density)
        carlist=random.sample(range(self.length*self.lane),num_of_cars)
        for car in carlist:
            self.current_state[int(car/self.length)][car%self.length]=0
        self.next_state=self.array_generate()
        self.flowcount=0

    def update(self):
        for lane_num in range(self.lane):
            for pos in range(self.length):
                if self.current_state[lane_num][pos]!=-1:
                    if self.checkspace_self(lane_num, pos)<self.current_state[lane_num][pos]+1:
                        lane_change=self.checkspace_other(lane_num,pos)
                        if lane_change==-1:
                            self.current_state[lane_num][pos],self.current_state[lane_num-1][pos]=-1,self.current_state[lane_num][pos]
                        elif lane_change==1:
                            self.current_state[lane_num][pos],self.current_state[(lane_num+1)%self.lane][pos]=-1,self.current_state[lane_num][pos]

        for lane_num in range(self.lane):
            for pos in range(self.length):
                if self.current_state[lane_num][pos]!=-1:
                    empty=self.checkspace_self(lane_num, pos)
                    if empty>self.current_state[lane_num][pos]:
                        self.current_state[lane_num][pos]+=1
                    elif empty<self.current_state[lane_num][pos]:
                        self.current_state[lane_num][pos]=empty
                    if self.current_state[lane_num][pos]>0:
                        if random.random()<self.probslow:
                            self.current_state[lane_num][pos]-=1

        for lane_num in range(self.lane):
            for pos in range(self.length):
                speed=int(self.current_state[lane_num][pos])
                if speed != -1:
                    self.next_state[lane_num][(pos + speed) % self.length]=speed
                    if (pos+speed)%self.length != pos+speed:
                        self.flowcount += 1
        self.current_state=self.next_state
        self.next_state= self.array_generate()

    def checkspace_self(self, lane_num, pos):
        empty=0
        for a in range(1,self.maxvelocity+1):
            if self.current_state[lane_num][(pos + a) % self.length]==-1:
                empty+=1
            else:
                break
        return empty

    def checkspace_other(self,lane_num, pos):
        front_empty_left=-1
        front_empty_right=-1
        back_empty_left=-1
        back_empty_right=-1

        for space in range(0,self.maxvelocity+1):
            if self.current_state[(lane_num+1)%self.lane][(int(pos) + space) % self.length]==-1:
                front_empty_right+=1
            else:
                break

        for space in range(0,self.maxvelocity+1):
            if self.current_state[lane_num-1][(pos + space) % self.length]==-1:
                front_empty_left+=1
            else:
                break

        for space in range(0,self.maxvelocity+1):
            if self.current_state[(lane_num+1)%self.lane][(int(pos) - space) % self.length]==-1:
                back_empty_right+=1
            else:
                break

        for space in range(0,self.maxvelocity+1):
            if self.current_state[lane_num-1][(pos - space) % self.length]==-1:
                back_empty_left+=1
            else:
                break

        if front_empty_left>=self.current_state[lane_num][pos]+1 and back_empty_left>=self.maxvelocity:
            return -1
        elif front_empty_right>=self.current_state[lane_num][pos]+1 and back_empty_right>=self.maxvelocity:
            return 1
        else:
            return 0


    def display(self):
        for lane_num in range(self.lane):
            print(''.join('.' if x==-1 else str(int(x)) for x in self.current_state[lane_num]))


    def simulate(self):
        self.initialize()
        self.display()
        print("")
        time.sleep(1)
        for i in range(self.steps):
            self.update()
            self.display()
            print("")
            time.sleep(1)

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

    def draw(self):
        plt.ylim(-5,5)
        if self.lane==1:
            #plt.hlines([0.5,-0.5], xmin=0, xmax=self.length,color="black")
            for pos in range(self.length):
                plt.scatter(pos,0,s=2,marker="s",color="white" if int(self.current_state[0][pos])==-1 else "black")

        elif self.lane==2:
            plt.hlines([-1,0,1], xmin=0, xmax=self.length, color="black")
            for lane in range(self.lane):
                for pos in range(self.length):
                    plt.scatter(pos, 0.5 if lane==0 else -0.5, s=2, marker="s",color="white" if int(self.current_state[lane][pos]) == -1 else "black")
        else:
            print("Lanes more than 2 unavailable.")




Simulator1=TrafficSimulation(length=100,density=0.13,maxvelocity=5,probslow=0.5,steps=50,times=20,lane=2)
#Simulator1.simulate()

import pycxsimulator
pycxsimulator.GUI().start(func=[Simulator1.initialize, Simulator1.draw, Simulator1.update])