import os
import shutil
from numpy import average
import sc2reader
import matplotlib.pyplot as plt
from functions.prettyPrinter import formatReplay
import matplotlib.pyplot as plt

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
                length_of_game = replay.frames // 22.404

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

                logWorker(file, replay.filename, wc,wc2, replay.player, pid, pid2, length_of_game, replay.start_time)

        except Exception as e:
            print(e)

    print('promedio')
    print( average(avg))
    print( average(avg2))

def logWorker(file, fileName, wc,wc2, playerDict, pid, pid2, length, date):

    result = playerDict[pid].result
    p1 = playerDict[pid].name
    p2 = playerDict[pid2].name
    r1 = playerDict[pid].pick_race
    r2 = playerDict[pid2].pick_race


    file.write(result + '\t' + str(wc) + '\t' + str(wc2) + '\t' + p1 + '\t' + p2 + '\t' +
        r1 + '\t' + r2 + '\t' + str(length) + '\t' + str(date) + '\t' +  fileName + '\t' + '\n')
    # file.write("player 1: " + str(worker_counter(replay, sec, 1)) + '\n')
    # file.write("player 2: " + str(worker_counter(replay, sec, 2)) + '\n')
    # file.write(str(length_of_game/60) + '\n')
    # file.write(str(replay.frames) + '\n')

def graphWorker(replay):
    length_of_game = replay.frames // 22.404
    event_names = set([event.name for event in replay.events])
    events_of_type = {name: [] for name in event_names}
    for event in replay.events:
        events_of_type[event.name].append(event)
    workers_1 = [worker_counter2(events_of_type, k, 1) for k in range(int(length_of_game)+1)]
    workers_2 = [worker_counter2(events_of_type, k, 2) for k in range(int(length_of_game)+1)]

    plt.figure()
    plt.plot(workers_1, label=replay.players[0])
    plt.plot(workers_2, label=replay.players[1])
    plt.legend(loc=2)
    plt.show()


def copy_replay(file:str, replay, save_path:str):
    print(file)
    print(os.path.basename(file))
    new_name = f"{save_path}{replay.length}_{os.path.splitext(os.path.basename(file))[0]}_{replay.filehash[-10:]}.SC2Replay"
    shutil.copy(file,new_name)

def analize_drone_kills(replay, opponent_uid):
    event_names = set([event.name for event in replay.events])
    events_of_type = {name: [] for name in event_names}
    for event in replay.events:
        events_of_type[event.name].append(event)
    unit_die_events = events_of_type["UnitDiedEvent"]
    for event in unit_die_events:
        if event.killing_player is None:
            continue
        if event.killing_player.detail_data["bnet"]["uid"] != opponent_uid:
            continue
        if event.second/60 > 10:
            continue
        if "Mineral" in event.unit.name:
            continue
        if event.unit.name != "Drone":
            continue
        try:
            print(event.unit.name, event.killing_unit.name, event.second/60)
        except Exception as ex:
            print(ex)

def plot_drone_kills(replay):
    # create dictionary of events and their types
    event_names = set([event.name for event in replay.events])
    events_of_type = {name: [] for name in event_names}
    for event in replay.events:
        events_of_type[event.name].append(event)

    length_of_game = replay.frames // 24

    workers_1 = [worker_counter(replay, k, 1) for k in range(length_of_game)]
    workers_2 = [worker_counter(replay, k, 2) for k in range(length_of_game)]

    plt.figure()
    plt.plot(workers_1, label=replay.players[0])
    plt.plot(workers_2, label=replay.players[1])
    plt.legend(loc=2)
    plt.figlegend
    plt.xlabel('seconds')
    plt.title(replay.filename)
    plt.show()
    # print(event)

def events_dic(replay):
    event_names = set([event.name for event in replay.events])
    events_of_type = {name: [] for name in event_names}
    for event in replay.events:
        events_of_type[event.name].append(event)
    return events_of_type


def drone_events(events):
    drone_born = []
    for event in events:
        if event.unit.name != "Drone":
            continue
        drone_born.append(event)
    return drone_born

def killed_events(events):
    filtered = []
    filtered_2 = []
    for event in events:
        if event.killer == None:
            filtered_2.append(event)
            continue
        filtered.append(event)
    return filtered, filtered_2
    ...

def return_ranges(events, minutes=10000):
    count = 0
    time = []
    event = []
    for b in events:
        if b.second/1.4/60 > minutes:
            continue
        time.append(b.second/1.4/60)
        event.append(count)
        count = count + 1
    return time, event

def return_total_worker_ranges(born, dead, minutes=10000):
    ut = born + dead
    newlist = sorted(ut, key=lambda x: x.second)
    total_count = []
    time_total = []
    count = 0
    for e in newlist:
        if e.second/1.4/60 > minutes:
            continue
        if e.name == 'UnitBornEvent':
            count = count + 1
        if e.name == 'UnitDiedEvent':
            count = count - 1
        time_total.append(e.second/1.4/60)
        total_count.append(count)
    return time_total, total_count


def worker_timeline(replay, minute_limit = 9):
    events = events_dic(replay)
    drone_born_events = drone_events(events["UnitBornEvent"])
    drone_dead_events = drone_events(events["UnitDiedEvent"])
    drone_killed_events, drone_build_events = killed_events(drone_dead_events)

    print(len(drone_born_events))

    time_born, worker_count = return_ranges(drone_born_events, minute_limit)
    time_dead, dead_count = return_ranges(drone_build_events, minute_limit)
    time_killed, killed_count = return_ranges(drone_killed_events, minute_limit)
    time_total, total_count = return_total_worker_ranges(drone_born_events,drone_dead_events, minute_limit)


    plt.figure(dpi=200)
    plt.plot(time_born, worker_count, 'bo', markersize=0.5)
    plt.plot(time_killed, killed_count, 'ro', markersize=0.5)
    plt.plot(time_dead, dead_count, 'yo', markersize=0.5)
    # plt.plot(time_total, total_count, drawstyle='steps-pre',markersize=0.5)
    # plt.plot(workers_2, label=replay.players[1])
    plt.legend(loc=2)
    plt.figlegend
    plt.xlabel('seconds')
    plt.margins(x=-0.4, y=-0.4)
    plt.xticks(range(0, 11, 1))
    plt.yticks(range(0, 140, 5))
    plt.grid()
    plt.title(replay.filename)
    plt.savefig(f"plot/{os.path.splitext(os.path.basename(replay.filename))[0]}.png")
    # plt.show()

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
# https://github.com/ZephyrBlu other libraries
# https://stackoverflow.com/questions/58372068/keep-watch-on-a-folder-for-recently-added-file-and-display-the-data-inside-that