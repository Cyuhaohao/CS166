import matplotlib
matplotlib.use('TkAgg')
from pylab import *
import random
import math
n = 61


def paint(x, y):
    global config
    for a in range(x - 2, x + 3):
        for b in range(y - 2, y + 3):
            config[a, b] = 1
    if random.random()<0.15:
        for a in range(x - 1, x + 2):
            for b in range(y - 1, y + 2):
                config[a, b] = 0


def select(x, y):
    while True:
        a = random.randint(x - 5, x + 5)
        b = random.randint(y - 5, y + 5)
        if abs(x - a) != 5 or abs(y - b) != 5:
            break
    return [a, b]


def locate_start():
    for a in range(n):
        for b in range(n):
            if config[a,b]!=0:
                return [a,b]


def initialize():
    global config, selected, current_place, num_space, num_cleaned, prob_cleaned
    config = zeros([n, n])
    selected = [0] * 63
    selected[0] = ([int((n - 1) / 2), int((n - 1) / 2)])

    for i in range(1, 63):
        x = selected[int(math.ceil(i / 2) - 1)][0]
        y = selected[int(math.ceil(i / 2) - 1)][1]
        selected[i] = select(x, y)

    for k in selected:
        paint(k[0], k[1])

    num_space = 0
    num_cleaned = 1

    for a in range(n):
        for b in range(n):
            if config[a, b] != 0:
                num_space += 1

    prob_cleaned = []
    prob_cleaned.append(num_cleaned / num_space)

    current_place=locate_start()
    config[current_place[0], current_place[1]]=0.25


def observe():
    global config
    subplot(1, 2, 1)
    cla()
    imshow(config, vmin=0, vmax=1, cmap=cm.binary)
    subplot(1, 2, 2)
    plot(prob_cleaned)


def move(next_step):
    global config, current_place, num_cleaned, prob_cleaned
    config[current_place[0], current_place[1]] = 0.25
    if next_step == 1:
        if config[current_place[0] - 1, current_place[1]] == 1:
            num_cleaned += 1
        config[current_place[0] - 1, current_place[1]] = 0.6
        current_place = [current_place[0] - 1, current_place[1]]
    if next_step == 2:
        if config[current_place[0], current_place[1] + 1] == 1:
            num_cleaned += 1
        config[current_place[0], current_place[1] + 1] = 0.6
        current_place = [current_place[0], current_place[1] + 1]
    if next_step == 3:
        if config[current_place[0] + 1, current_place[1]] == 1:
            num_cleaned += 1
        config[current_place[0] + 1, current_place[1]] = 0.6
        current_place = [current_place[0] + 1, current_place[1]]
    if next_step == 4:
        if config[current_place[0], current_place[1] - 1] == 1:
            num_cleaned += 1
        config[current_place[0], current_place[1] - 1] = 0.6
        current_place = [current_place[0], current_place[1] - 1]

    if next_step == 5:
        if config[current_place[0] - 1, current_place[1]+1] == 1:
            num_cleaned += 1
        config[current_place[0] - 1, current_place[1]+1] = 0.6
        current_place = [current_place[0] - 1, current_place[1]+1]
    if next_step == 6:
        if config[current_place[0] + 1, current_place[1]+1] == 1:
            num_cleaned += 1
        config[current_place[0] + 1, current_place[1]+1] = 0.6
        current_place = [current_place[0] + 1, current_place[1]+1]
    if next_step == 7:
        if config[current_place[0] + 1, current_place[1]-1] == 1:
            num_cleaned += 1
        config[current_place[0] + 1, current_place[1]-1] = 0.6
        current_place = [current_place[0] + 1, current_place[1]-1]
    if next_step == 8:
        if config[current_place[0] - 1, current_place[1]-1] == 1:
            num_cleaned += 1
        config[current_place[0] - 1, current_place[1]-1] = 0.6
        current_place = [current_place[0] - 1, current_place[1]-1]
    prob_cleaned.append(num_cleaned / num_space)

def check_next(x, y):
    nextlist = []
    if config[x-1, y] != 0:
        nextlist.append(1)
    if config[x, y+1] != 0:
        nextlist.append(2)
    if config[x+1, y] != 0:
        nextlist.append(3)
    if config[x, y-1] != 0:
        nextlist.append(4)

    if config[x - 1, y+1] != 0:
        nextlist.append(5)
    if config[x + 1, y+1] != 0:
        nextlist.append(6)
    if config[x + 1, y-1] != 0:
        nextlist.append(7)
    if config[x - 1, y-1] != 0:
        nextlist.append(8)
    return nextlist


def check_next_remember(x, y):
    nextlist = []
    if config[x-1, y] == 1:
        nextlist.append(1)
    if config[x, y+1] == 1:
        nextlist.append(2)
    if config[x+1, y] == 1:
        nextlist.append(3)
    if config[x, y-1] == 1:
        nextlist.append(4)
    return nextlist


class RandomMove():
    def __init__(self):
        initialize()

    def next_step(self,x, y):
        nextlist=check_next(x,y)
        return random.sample(nextlist, 1)[0]

    def update(self):
        global config, current_place, num_cleaned, prob_cleaned
        current_direction = self.next_step(current_place[0], current_place[1])
        move(current_direction)


class RandomBounce():
    def __init__(self):
        initialize()
        self.current_direction=random.randint(1,8)

    def next_step(self,x, y,current_direction):
        nextlist = check_next(x,y)
        if current_direction in nextlist:
            return current_direction
        else:
            return random.sample(nextlist, 1)[0]

    def update(self):
        global config, current_place, num_cleaned, prob_cleaned
        self.current_direction=self.next_step(current_place[0], current_place[1],self.current_direction)
        move(self.current_direction)


class WallFollow():
    def __init__(self):
        initialize()
        self.current_direction=check_next_remember(current_place[0], current_place[1])[0]
        self.movestate='wall'

    def next_step(self):
        nextlist=check_next_remember(current_place[0], current_place[1])
        if [1,2,3,4][self.current_direction-2] in nextlist:
            self.current_direction = [1,2,3,4][self.current_direction-2]
        elif [1,2,3,4][self.current_direction-1] in nextlist:
            self.current_direction = [1,2,3,4][self.current_direction-1]
        elif [1,2,3,4][self.current_direction%4] in nextlist:
            self.current_direction = [1,2,3,4][self.current_direction%4]
        else:
            self.current_direction = [1,2,3,4][(self.current_direction+1)%4]

    def bounce_next_step(self,x, y,current_direction):
        nextlist = check_next(x,y)
        if current_direction in nextlist:
            return current_direction
        else:
            return random.sample(nextlist, 1)[0]

    def update(self):
        global config, current_place, num_cleaned, prob_cleaned
        if len(check_next_remember(current_place[0], current_place[1]))!=0:
            if self.movestate=='bounce':
                self.current_direction = check_next_remember(current_place[0], current_place[1])[0]
                self.movestate='wall'
            self.next_step()
            move(self.current_direction)
        else:
            self.movestate='bounce'
            self.current_direction = self.bounce_next_step(current_place[0], current_place[1], self.current_direction)
            move(self.current_direction)






# randommove1=RandomMove()
# randombounce1=RandomBounce()
wallfollow1=WallFollow()

from CS166 import pycxsimulator
pycxsimulator.GUI().start(func=[initialize, observe, wallfollow1.update])



# Calculate the average space in the room

# space_list=[]
# for i in range(10000):
#     initialize()
#     space_list.append(num_space)
#
# hist(space_list)
# print(mean(space_list))
# show()



# Monte Carlo Simulation for different algorithms


def test(instance):
    k=0
    result_set=[0]*2
    for i in range(5000):
        instance.update()
        if i==1499:
            k+=1
            result_set[0]=prob_cleaned[-1]
        if result_set[1]==0:
            if prob_cleaned[-1]>=0.8:
                k+=1
                result_set[1]=i
        if i==4999 and result_set[1]==0:
            result_set[1]=5000
        if k==2:
            break
    return result_set


def plot_generate(instance,name):
    global result_prob,result_steps
    space_list=[]
    result_prob=[]
    result_steps=[]
    for i in range(3000):
        initialize()
        space_list.append(num_space)
        result_set=test(instance)
        result_prob.append(result_set[0])
        result_steps.append(result_set[1])
    hist(result_prob,alpha=0.5,color="red",bins=50)
    title(''.join(["Distribution of proportion of cleaned area after 1500 steps (",name,")"]))
    xlabel("Proportion of the cleaned area")
    ylabel("Times of certain proportions")
    show()
    hist(result_steps,alpha=0.5,bins=50)
    title(''.join(["Distribution of steps when 80% of the room is clean (",name,")"]))
    xlabel("Steps when 80% of the room is clean")
    ylabel("Times of certain steps")
    show()
    print("Result for %s algorithm" % name)
    print("95% confidence interval of proportion:",percentile(result_prob,2.5),"to",percentile(result_prob,97.5))
    print("Mean value of proportion:",mean(result_prob))
    print("95% confidence interval of steps:",percentile(result_steps,2.5),"to",percentile(result_steps,97.5))
    print("Mean value of steps:",mean(result_steps))
    print("Number of steps needed to clean one unit space:",mean(result_steps)/(0.8*mean(space_list)),"\n")

#
#
# wallfollow = WallFollow()
# plot_generate(wallfollow,"Wall Follow")
# prob_wallfollow=result_prob
# steps_wallfollow=result_steps
#
#
# randommove=RandomMove()
# plot_generate(randommove,"Random Move")
# prob_randommove=result_prob
# steps_randommove=result_steps
#
#
# randombounce=RandomBounce()
# plot_generate(randombounce,"Random Bounce")
# prob_randombounce=result_prob
# steps_randombounce=result_steps
#
#
# hist(prob_wallfollow,label="Wall Follow",alpha=0.5,color="red",bins=50)
# hist(prob_randombounce,label="Random Bounce",alpha=0.5,color="green",bins=50)
# hist(prob_randommove,label="Random Move",alpha=0.5,color="blue",bins=50)
# legend()
# title("Proportion of cleaned area after 1500 steps")
# xlabel("Proportion of the cleaned area")
# ylabel("Times of certain proportions")
# show()
#
#
# hist(steps_wallfollow,label="Wall Follow",alpha=0.5,color="red",bins=50)
# hist(steps_randombounce,label="Random Bounce",alpha=0.5,color="green",bins=50)
# hist(steps_randommove,label="Random Move",alpha=0.5,color="blue",bins=50)
# legend()
# title("Distribution of steps when 80% of the room is clean")
# xlabel("Steps when 80% of the room is clean")
# ylabel("Times of certain steps")
# show()