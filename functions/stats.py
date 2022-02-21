import os
from numpy import average
import sc2reader
import matplotlib.pyplot as plt

from prettyPrinter import formatReplay


path = 'C:/Users/loren/Documents/StarCraft II/Accounts/66185323/1-S2-2-818362/Replays/Multiplayer/'

def worker_counter(replay, sec, player_id):

    frame = sec * 22.404
    workers = []
    for event in replay.events:
        if event.name == "UnitBornEvent" and event.control_pid == player_id:
            if event.unit.is_worker:
                workers.append(event.unit)
    
        if event.name == "UnitDiedEvent":
            if event.unit in workers:
                workers.remove(event.unit)
        
        if event.frame > frame:
            break
    
    return len(workers)

def worker_counter2(events, sec, player_id):
    frame = sec * 22.404

    unit_born_events = events["UnitBornEvent"]
    unit_died_events = events["UnitDiedEvent"]

    workers = []

    for e in unit_born_events:

        if e.control_pid == player_id and e.unit.is_worker and e.frame < frame:
            workers.append(e.unit)
            
    for e in unit_died_events:

        if e.unit in workers and e.frame < frame:
            workers.remove(e.unit)
    return len(workers)

def getMyTeamnumber(replay, name):        
    for key in replay.player:
        
        if replay.player[key].name == name:
            return replay.player[key].pid

def getKey(replay, name):
    for key in replay.player:
        
        if replay.player[key].name == name:
            return key
            
def printName(replay):

    if replay.is_ladder:
        
        print(replay.player[1].name)
        print(replay.player[1].pick_race)
        print(replay.player[1].pid)
        print(replay.player[1].result)
    


def avgWorkerAtSec(file, sec):
    path = 'C:/Users/loren/Documents/StarCraft II/Accounts/66185323/1-S2-2-818362/Replays/Multiplayer/'
    files = os.listdir(path)
    avg = []
    avg2 = []
    
    for f in files:
        try:
            replay = sc2reader.load_replay(path + f, load_map=False)


            if replay.is_ladder and replay.type == '1v1' and replay.frames > (sec * 22.404):                                        
                # create dictionary of events and their types
                event_names = set([event.name for event in replay.events])
                events_of_type = {name: [] for name in event_names}
                for event in replay.events:
                    events_of_type[event.name].append(event)

                pid = getMyTeamnumber(replay,'VanKiwi')
                if pid ==1:
                    pid2 = 2
                else:
                    pid2 = 1

                # print(formatReplay(replay))
                wc = worker_counter2(events_of_type, 360, pid)
                avg.append(wc)
                wc2 = worker_counter2(events_of_type, 360, pid2)
                avg2.append(wc2)

                logWorker(file, replay.filename, wc,wc2, replay.player[pid].name, replay.player[pid2].name, replay.player[pid].result)
               
        except Exception as e:
            print(e)

    print('promedio')
    print( average(avg))
    print( average(avg2))


def logWorker(file, fileName, wc,wc2, p1, p2, result):    
    
        
    file.write(result + '\t' + str(wc) + '\t' + str(wc2) + '\t' + p1 + '\t' + p2 + '\t' + fileName + '\t' + '\n')
    # file.write("player 1: " + str(worker_counter(replay, sec, 1)) + '\n')
    # file.write("player 2: " + str(worker_counter(replay, sec, 2)) + '\n')
    # file.write(str(length_of_game/60) + '\n')
    # file.write(str(replay.frames) + '\n')

def graphWorker(replay):
    length_of_game = replay.frames // 22.404
    workers_1 = [worker_counter(replay, k, 1) for k in range(int(length_of_game)+1)]
    workers_2 = [worker_counter(replay, k, 2) for k in range(int(length_of_game)+1)]

    plt.figure()
    plt.plot(workers_1, label=replay.players[0])
    plt.plot(workers_2, label=replay.players[1])
    plt.legend(loc=2)
    plt.show()


# unit_born_events = events_of_type["UnitBornEvent"]

# for ube in unit_born_events:

#     if ube.unit.name != "InvisibleTargetDummy":
        
#         print("{} created {} at second {}".format(ube.unit_controller,
#             ube.unit,
#             ube.second))

# unit_init_events = events_of_type["UnitInitEvent"]

# for uie in unit_init_events:
#     print("{} started creating {} at second {}".format(uie.unit_controller,
#                                                        uie.unit,
#                                                        uie.second))

# unit_done_events = events_of_type["UnitDoneEvent"]

# for ude in unit_done_events:
#     print("{} finished".format(ude.unit))

# unit_died_events = events_of_type["UnitDiedEvent"]

# for udiede in unit_died_events:
#     print("{} was killed by {} using {} at ({}, {})".format(udiede.unit,
#                                                             udiede.killer,
#                                                             udiede.killing_unit,
#                                                             udiede.x,
#                                                             udiede.y))

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

