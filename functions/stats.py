import os
import shutil
import matplotlib.pyplot as plt
from functions.prettyPrinter import formatReplay

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

def copy_replay(file:str, replay, save_path:str):
    print(file)
    print(os.path.basename(file))
    new_name = f"{save_path}{replay.length}_{os.path.splitext(os.path.basename(file))[0]}_{replay.filehash[-10:]}.SC2Replay"
    shutil.copy(file,new_name)

def analize_drone_kills(replay, opponent_uid):
    events_of_type = events_dic(replay)
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

def events_dic(replay):
    event_names = set([event.name for event in replay.events])
    events_of_type = {name: [] for name in event_names}
    for event in replay.events:
        events_of_type[event.name].append(event)
    return events_of_type

def drone_events(events):
    filter_events = []
    for event in events:
        if event.unit_controller == None:
            continue
        print(event.unit_controller)
        # event.owner.name # player
        if event.unit.name != "Drone":
            continue
        filter_events.append(event)
    return filter_events

def filter_killed_events(events):
    filtered = []
    filtered_2 = []
    for event in events:
        if event.killer == None:
            filtered_2.append(event)
            continue
        filtered.append(event)
    # 2 casues of drone death, being killed, or being transform into building
    return filtered, filtered_2

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
    # merge two lists and sort by time, to manually count the actual worker count
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

def worker_timeline(replay, unit_name = "Drone", minute_limit = 9, uid = 0):
    events = events_dic(replay)
    born_events = [event for event in events["UnitBornEvent"] if event.unit.name  == unit_name and event.unit_controller.uid == uid]
    dead_events = [event for event in events["UnitDiedEvent"] if event.unit.name  == unit_name and event.unit.owner.uid == uid]
    killed_events, build_events = filter_killed_events(dead_events)
    print(len(born_events))
    print(replay.players[0], replay.players[1])
    plt.figure(dpi=200)
    plt.plot(*return_ranges(born_events, minute_limit), 'bo', markersize=0.5, label=f'{unit_name} born')
    plt.plot(*return_ranges(killed_events, minute_limit), 'ro', markersize=0.5, label=f'{unit_name} killed')
    plt.plot(*return_ranges(build_events, minute_limit), 'yo', markersize=0.5, label=f'{unit_name} transformed')
    plt.plot(*return_total_worker_ranges(born_events,dead_events, minute_limit), drawstyle='steps-pre',markersize=0.5)
    # plt.plot(workers_2, label=replay.players[1])
    plt.legend(loc=2)
    plt.figtext(0.5, 0.01, f"{replay.players[0]}{replay.players[1]}", wrap=True, horizontalalignment='center', fontsize=12)
    plt.margins(x=-0.4, y=-0.4)
    plt.xticks(range(0, 11, 1))
    plt.yticks(range(0, 140, 5))
    plt.grid()
    title = f"[{replay.filename.split('/')[-1].split('.')[0]}] {replay.players[0].name} vs {replay.players[1].name}"
    plt.title(title)
    # plt.savefig(f"plot/{os.path.splitext(os.path.basename(replay.filename))[0]}.png")
    plt.show()

def print_events(events_of_type):
    unit_born_events = events_of_type["UnitBornEvent"]

    for ube in unit_born_events:

        if ube.unit.name != "InvisibleTargetDummy":

            print("{} created {} at second {}".format(ube.unit_controller,
                ube.unit,
                ube.second))

    unit_init_events = events_of_type["UnitInitEvent"]

    for uie in unit_init_events:
        print("{} started creating {} at second {}".format(uie.unit_controller,
                                                           uie.unit,
                                                           uie.second))

    unit_done_events = events_of_type["UnitDoneEvent"]

    for ude in unit_done_events:
        print("{} finished".format(ude.unit))

    unit_died_events = events_of_type["UnitDiedEvent"]

    for udiede in unit_died_events:
        print("{} was killed by {} using {} at ({}, {})".format(udiede.unit,
                                                                udiede.killer,
                                                                udiede.killing_unit,
                                                                udiede.x,
                                                                udiede.y))

# python .\prettyPrinter.py "C:\Users\loren\Documents\StarCraft II\Accounts\66185323\1-S2-2-818362\Replays\Multiplayer\Blackburn LE (47).SC2Replay"
# https://www.miguelgondu.com/blogposts/2018-09-03/a-tutorial-on-sc2reader-events-and-units/
# https://github.com/ZephyrBlu other libraries
# https://stackoverflow.com/questions/58372068/keep-watch-on-a-folder-for-recently-added-file-and-display-the-data-inside-that