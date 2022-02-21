from functions.stats import avgWorkerAtSec, worker_counter, graphWorker, logWorker
from prettyPrinter import formatReplay
import sc2reader
import matplotlib.pyplot as plt
import os

path = 'C:/Users/loren/Documents/StarCraft II/Accounts/66185323/1-S2-2-818362/Replays/Multiplayer/'
file = 'Pride of Altaris LE (6).SC2Replay'

f = open("workerslost.txt", "a")
f.write("Now the file has more content!")
replay = sc2reader.load_replay(path + file, load_map=False)

avgWorkerAtSec(f,360)
# logWorker(replay,f, 360)
# graphWorker(replay)

f.close()

# replay = sc2reader.load_replay(path + file, load_map=False)

# create dictionary of events and their types
# event_names = set([event.name for event in replay.events])
# events_of_type = {name: [] for name in event_names}
# for event in replay.events:
#     events_of_type[event.name].append(event)

# unit_born_events = events_of_type["UnitBornEvent"]

# unit_init_events = events_of_type["UnitInitEvent"]

# unit_done_events = events_of_type["UnitDoneEvent"]

# unit_died_events = events_of_type["UnitDiedEvent"]

# length_of_game = replay.frames // 24



# workers_1 = [worker_counter(replay, k, 1) for k in range(length_of_game)]
# workers_2 = [worker_counter(replay, k, 2) for k in range(length_of_game)]

# plt.figure()
# plt.plot(workers_1, label=replay.players[0])
# plt.plot(workers_2, label=replay.players[1])
# plt.legend(loc=2)
# plt.show()
# print(event)



# python .\prettyPrinter.py "C:\Users\loren\Documents\StarCraft II\Accounts\66185323\1-S2-2-818362\Replays\Multiplayer\Blackburn LE (47).SC2Replay"
# https://www.miguelgondu.com/blogposts/2018-09-03/a-tutorial-on-sc2reader-events-and-units/

# TODO 6 minutes metrics
# how many workers did I loose on the first 6 minutes
# how long does it take to the get 3thre base saturation?
# how long to max out? 8:00 max roach metric
# what types of units kill my drones? adepts? reaper? liberator? hellions?
# worker graphs
# creep tumor count
# overlord spread
# overseer changeling

# basic build opener of my oponent

# analize builds I loose to the most
# analize map records

# control group management - hard to analize
# analize my scouts - hard
# check location of enemy tech on the position of my units and vision? hard
# camera movements? how long does it take to respond to an attack or harrasment
# detect misclicks? hard

# make it run in the background
# save data in a database
# sort my replays and rename them 

