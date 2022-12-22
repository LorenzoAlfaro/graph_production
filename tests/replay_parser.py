from functions.stats import avgWorkerAtSec, worker_counter, graphWorker, logWorker
from functions.prettyPrinter import formatReplay
import sc2reader
import matplotlib.pyplot as plt
import os

path = 'C:/Users/loren/Documents/StarCraft II/Accounts/66185323/1-S2-2-818362/Replays/Multiplayer/'
file = 'Pride of Altaris LE (6).SC2Replay'

f = open("workerslost.txt", "a")
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

