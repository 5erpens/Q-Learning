import os
import matplotlib.pyplot as plt
from matplotlib import style

style.use('fivethirtyeight')
fig = plt.figure()
plt2 = plt.twinx()
ax = fig.add_subplot(1,1,1)
ax2 = fig.add_subplot(1,1,1)


def animate(i):
    xs = []
    ys = []
    zs = []
    es = []
    ss = []

    plt.clf()

    plt.xlabel('Episode')
    plt.ylabel('rewards')

    #plt2.ylabel('Reward')

    graph_data = open(os.getcwd() + '\graph.cache', 'r')

    for line in graph_data.readlines():
        if len(line) > 1:
            line = line.strip()
            x, y, z, e, s = line.split(',')
            xs.insert(len(xs), int(x))
            ys.insert(len(ys), int(y))
            zs.insert(len(zs), float(z))
            es.insert(len(es), float(e))
            ss.insert(len(ss), int(s))
    #plt.plot(xs, ys, linewidth=1) #steps
    plt.plot(xs, zs, linewidth=1) # rewards
    #plt.plot(xs, es, linewidth=1) # epsilon

animate(1)
plt.show()