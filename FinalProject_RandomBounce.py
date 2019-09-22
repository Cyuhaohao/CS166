import matplotlib

matplotlib.use('TkAgg')
from pylab import *
import random
import math


class RandomMove():
    def __init__(self):
        self.n = 61
        self.config = zeros([self.n, self.n])
        self.selected = [0] * 63
        self.num_space = 0
        self.num_cleant = 1
        self.prob_cleant = []
        self.current_place=[0,0]

    def select(self, x, y):
        while True:
            a = random.randint(x - 5, x + 5)
            b = random.randint(y - 5, y + 5)
            if abs(x - a) != 5 or abs(y - b) != 5:
                break
        return [a, b]

    def paint(self,x, y):
        for a in range(x - 2, x + 3):
            for b in range(y - 2, y + 3):
                self.config[a, b] = 1

    def initialize(self):
        self.config = zeros([self.n, self.n])
        self.selected = [0] * 63
        self.num_space = 0
        self.num_cleant = 1
        self.prob_cleant = []
        self.current_place=[0,0]
        self.selected[0] = ([int((self.n - 1) / 2), int((self.n - 1) / 2)])
        for i in range(1, 63):
            x = self.selected[int(math.ceil(i / 2) - 1)][0]
            y = self.selected[int(math.ceil(i / 2) - 1)][1]
            self.selected[i] = self.select(x, y)

        for k in self.selected:
            self.paint(k[0], k[1])

        for a in range(self.n):
            for b in range(self.n):
                if self.config[a, b] != 0:
                    self.num_space += 1

        self.prob_cleant.append(self.num_cleant / self.num_space)
        self.config[int((self.n - 1) / 2), int((self.n - 1) / 2)] = 0.85
        self.current_place = [int((self.n - 1) / 2), int((self.n - 1) / 2)]

    def observe(self):
        subplot(1, 2, 1)
        cla()
        imshow(self.config, vmin=0, vmax=1, cmap=cm.binary)
        subplot(1, 2, 2)
        plot(self.prob_cleant)



    def check_next(self,x, y):
        nextlist = []
        if self.config[x, y - 1] != 0:
            nextlist.append(1)
        if self.config[x + 1, y] != 0:
            nextlist.append(2)
        if self.config[x, y + 1] != 0:
            nextlist.append(3)
        if self.config[x - 1, y] != 0:
            nextlist.append(4)
        return nextlist

    def update_randommove(self):
        next_step = random.sample(self.check_next(self.current_place[0], self.current_place[1]), 1)[0]
        self.config[self.current_place[0], self.current_place[1]] = 0.25

        if next_step == 1:
            if self.config[self.current_place[0], self.current_place[1] - 1] == 1:
                self.num_cleant += 1
            self.config[self.current_place[0], self.current_place[1] - 1] = 0.85
            self.current_place = [self.current_place[0], self.current_place[1] - 1]
        if next_step == 2:
            if self.config[self.current_place[0] + 1, self.current_place[1]] == 1:
                self.num_cleant += 1
            self.config[self.current_place[0] + 1, self.current_place[1]] = 0.85
            self.current_place = [self.current_place[0] + 1, self.current_place[1]]
        if next_step == 3:
            if self.config[self.current_place[0], self.current_place[1] + 1] == 1:
                self.num_cleant += 1
            self.config[self.current_place[0], self.current_place[1] + 1] = 0.85
            self.current_place = [self.current_place[0], self.current_place[1] + 1]
        if next_step == 4:
            if self.config[self.current_place[0] - 1, self.current_place[1]] == 1:
                self.num_cleant += 1
            self.config[self.current_place[0] - 1, self.current_place[1]] = 0.85
            self.current_place = [self.current_place[0] - 1, self.current_place[1]]
        self.prob_cleant.append(self.num_cleant / self.num_space)

    def update_random_bounce(self):
        pass




from CS166 import pycxsimulator
random1=RandomMove()
pycxsimulator.GUI().start(func=[random1.initialize, random1.observe, random1.update_randommove()])


# class RandomBounce():
