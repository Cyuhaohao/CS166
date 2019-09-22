import random
import numpy
import matplotlib.pyplot as plt



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
        print("\n")
        for i in range(self.steps):
            self.update()
            self.display()
            print("\n")

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


#Simulator1=TrafficSimulation(length=100,density=0.13,maxvelocity=5,probslow=0.5,steps=50,times=20,lane=2)
#Simulator1.simulate()


flowrate_list1_1=[]
flowrate_list1_2=[]
density_list1_1=[]
density_list1_2=[]

for den in range(1,101):
    density=float(den/100)
    Simulator=TrafficSimulation(length=50,density=density,maxvelocity=5,probslow=0.5,steps=300,times=10,lane=1)
    flowcounts=Simulator.flow_analysis()
    flowrate_list1_1.append(numpy.mean(flowcounts))
    density_list1_1.append(density)
    flowrate_list1_2.append(flowcounts)
    for i in range(len(flowcounts)):
        density_list1_2.append(density)
    print("\r", "Processing... <", "="*den, " "*(100-den), ">", den, "%")


flowrate_list2_1=[]
flowrate_list2_2=[]
density_list2_1=[]
density_list2_2=[]

for den in range(1,101):
    density=float(den/100)
    Simulator=TrafficSimulation(length=50,density=density,maxvelocity=5,probslow=0.5,steps=300,times=10,lane=2)
    flowcounts=Simulator.flow_analysis()
    flowrate_list2_1.append(numpy.mean(flowcounts))
    density_list2_1.append(density)
    flowrate_list2_2.append(flowcounts)
    for i in range(len(flowcounts)):
        density_list2_2.append(density)
    print("Situation2 density %f has finished." % density)


plt.xlabel("Density [cars per site]")
plt.ylabel("Flow [cars per time step]")
plt.title("Simulation")

plt.plot(density_list1_1, flowrate_list1_1, label="1 lane", c="red")
plt.scatter(density_list1_2, flowrate_list1_2, s=3, c="blue")

plt.plot(density_list2_1, flowrate_list2_1, label="2 lanes", c="yellow")
plt.scatter(density_list2_2, flowrate_list2_2, s=3, c="green")

plt.legend()
plt.show()

plt.xlabel("Density [cars per site]")
plt.ylabel("Flow Difference [cars per time step]")
plt.title("Difference between 1-lane and 2-lane")

differences=[]
for i in range(len(flowrate_list2_1)):
    differences.append(flowrate_list2_1[i]-flowrate_list1_1[i])
plt.plot(density_list1_1, differences)
plt.show()

