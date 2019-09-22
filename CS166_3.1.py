# Simple CA simulator in Python
#
# *** Hosts & Pathogens ***
#
# Copyright 2008-2012 Hiroki Sayama
# sayama@binghamton.edu

# Modified to run with Python 3

import matplotlib

matplotlib.use('TkAgg')

import pylab as PL
import random as RD
import scipy as SP

RD.seed()

width = 50
height = 50
initProb = 0.1
infectionRate = 0.15
regrowthRate = 0.85


def init():
    global time, config, nextConfig,m1,m2

    time = 0

    config = SP.zeros([height, width])
    for x in range(width):
        for y in range(height):
            if RD.random() < initProb:
                state = 2
            else:
                state = 1
            config[y, x] = state

    nextConfig = SP.zeros([height, width])
    m1=[]
    m2=[]


def draw():
    PL.subplot(1,3,1)
    PL.cla()
    PL.pcolor(config, vmin=0, vmax=2, cmap=PL.cm.jet)
    PL.axis('image')
    PL.title('t = ' + str(time))
    PL.subplot(1,3,2)
    m1.append(float(count(config)[1]/2500))
    m2.append(float(count(config)[0]/2500))
    PL.plot(m1)
    PL.title("Proportion of Healthy Hosts")
    PL.subplot(1,3,3)
    PL.plot(m2)
    PL.title("Proportion of Infected Hosts")


def step():
    global time, config, nextConfig

    time += 1

    for x in range(width):
        for y in range(height):
            state = config[y, x]
            if state == 0:
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        if config[(y + dy) % height, (x + dx) % width] == 1:
                            if RD.random() < regrowthRate:
                                state = 1
            elif state == 1:
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        if config[(y + dy) % height, (x + dx) % width] == 2:
                            if RD.random() < infectionRate:
                                state = 2
            else:
                state = 0

            nextConfig[y, x] = state

    config, nextConfig = nextConfig, config

def count(ar):
    k=0
    l=0
    for a in ar:
        for b in a:
            if b==2:
                k+=1
            if b==1:
                l+=1
    return k,l


import pycxsimulator

pycxsimulator.GUI().start(func=[init, draw, step])