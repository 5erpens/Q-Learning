import os
import sys

import matplotlib.pyplot as plt
from matplotlib import style
from queue import Queue

style.use('fivethirtyeight')
fig = plt.figure()
plt2 = plt.twinx()


def animate(average_set):
    xq = Queue()
    yq = Queue()
    zq = Queue()
    eq = Queue()
    sq = Queue()

    xs = []
    ys = []
    zs = []
    es = []
    ss = []

    plt.clf()

    plt.xlabel('Episode')
    plt.ylabel('Reward trend')

    # plt2.ylabel('Reward')

    graph_data = open(os.getcwd() + '\etemp.cache', 'r')

    for line in graph_data.readlines():
        if len(line) > 1:
            line = line.strip()
            x, y, z, e, s = line.split(',')
            xq.put(int(x))
            yq.put(float(y))
            zq.put(float(z))
            eq.put(float(e))
            sq.put(int(s))

    while not yq.empty():
        state_val = 0
        reward_val = 0
        count = 0
        episode_val = xq.get()
        flag = True
        for i in range(average_set):
            if yq.empty() or zq.empty():
                break
            else:
                count += 1
                state_val += yq.get()
                reward_val += zq.get()
                if flag:
                    flag = False
                else:
                    xq.get()
        xs.insert(len(xs), episode_val)
        ys.insert(len(ys), state_val/count)
        zs.insert(len(zs), reward_val/count)

    #plt.plot(xs, ys, linewidth=1) #steps trend
    plt.plot(xs, zs, linewidth=1) #reward trend


animate(int(input("average value: ")))
plt.show()
