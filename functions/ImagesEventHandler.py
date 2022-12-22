from asyncio import TimerHandle
import os
from PIL import Image
from PIL.ImageOps import grayscale
from watchdog.events import RegexMatchingEventHandler
from functions.stats import avgWorkerAtSec, getMyTeamnumber, worker_counter, graphWorker, logWorker, worker_counter2
import sc2reader as sc2
import time

class ImagesEventHandler(RegexMatchingEventHandler):
    THUMBNAIL_SIZE = (128, 128)
    IMAGES_REGEX = [r".*[^_thumbnail]\.jpg$"]

    def __init__(self):
        # super().__init__(self.IMAGES_REGEX)
        super().__init__()

    def on_created(self, event):
        filename, ext = os.path.splitext(event.src_path)
        print('created ' + filename +"  " + ext)
        time.sleep(1)
        self.newReplay(filename + ext)
        # self.process(event)

    def process(self, event):
        filename, ext = os.path.splitext(event.src_path)
        filename = f"{filename}_thumbnail.jpg"

        image = Image.open(event.src_path)
        image = grayscale(image)
        image.thumbnail(self.THUMBNAIL_SIZE)
        image.save(filename)

    def newReplay(self, fileName):

        if ".writeCacheBackup" in fileName:
            print("not a replay file")
            return
        
        replay = sc2.load_replay(fileName, load_map=False)
        # print(dir(replay.players[0]))
        print(replay.players[0].url)
        print("uid",replay.players[0].uid)
        # print("team_id",replay.players[0].teamd_id)
        print(replay.players[0].team)
        print("subregion", replay.players[0].subregion)
        print("sid",replay.players[0].sid)
        print("region",replay.players[0].region)
        print("recorder", replay.players[0].recorder)
        print("pid",replay.players[0].pid)
        print("name",replay.players[0].name)
        print("messages",replay.players[0].messages)
        print("highest league", replay.players[0].highest_league)
        print("detail",replay.players[0].detail_data)
        print("clan tag",replay.players[0].clan_tag)        
        
        # graphWorker(replay)

        # if replay.is_ladder and replay.type == '1v1' and replay.frames > (sec * 22.404):                                        
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
            
        self.printWorkerCount(60,events_of_type,pid,pid2)
        self.printWorkerCount(120,events_of_type,pid,pid2)
        self.printWorkerCount(180,events_of_type,pid,pid2)
        self.printWorkerCount(240,events_of_type,pid,pid2)
        self.printWorkerCount(300,events_of_type,pid,pid2)
        self.printWorkerCount(360,events_of_type,pid,pid2)
        self.printWorkerCount(420,events_of_type,pid,pid2)            
        # logWorker(file, replay.filename, wc,wc2, replay.player, pid, pid2, length_of_game, replay.start_time)
               
    def printWorkerCount(self,sec,events_of_type, pid, pid2):
        wc = worker_counter2(events_of_type, sec, pid)
        wc2 = worker_counter2(events_of_type, sec, pid2)
        print(sec,":", wc,"-",wc2)