import mysql.connector
from decouple import config
import os
import sc2reader as sc2
from sc2reader.objects import Player
from functions.stats import getMyTeamnumber, worker_counter2, logWorker
import traceback
import sys

# data = b'\xCE\xB1X'
# if isinstance(data, bytes):
#     print("true")
#     ...
# print(bytes.decode(b'\xCE\xB1X','utf-8'))
# print(bytes.decode(b'clan_tag','utf-8'))
# exit()
password = config('MYSQL_PASSWORD')
user = config('USER_NAME')
path = 'C:/Users/loren/Documents/StarCraft II/Accounts/66185323/1-S2-2-818362/Replays/Multiplayer/'
# path = 'C:/Users/loren/Documents/StarCraft II/Accounts/66185323/1-S2-1-1931022/Replays/Multiplayer/'

mydb = mysql.connector.connect(
    host="localhost",
    user=user,
    password=password,
    database="trainer",
    ssl_disabled=True
    )
mycursor = mydb.cursor()
# open folder of replays
files = os.listdir(path)
avg = []
avg2 = []
sec = 1 # second you are interesed at

for f in files:
    try:
        replay = sc2.load_replay(path + f, load_map = False)
        # print(f)
        if replay.type == '1v1' and replay.frames > (sec * 22.404):                                        
                                    
            p = replay.players[0]
            uid = p.detail_data['bnet']['uid']                        
            if uid == 818362 or uid == 1931022:
                p = replay.players[1]
                uid = p.detail_data['bnet']['uid']            
            if not p.is_human or uid == 6556840 or uid == 6795698 or uid == 5009518: # Lobo y Kinesin
                continue            
                        
            
            tag2 = "-"
            tag3 = "-"
            if p.clan_tag != "":
                
                tag2 = bytes(p.clan_tag, 'utf-8')
                tag3 = bytes.decode(tag2,'utf-8')
                print(tag3)                
                    
            sql = "INSERT INTO player_table (uid, player_name, clan_tag, region, subregion, player_url) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (uid, p.name, tag3, p.region, p.subregion, p.url)
            
            mycursor.execute(sql, val)
            mydb.commit()
            # print(p.name, p.result)
    except Exception as e:
        # raise e
        print("-------------------------------")
        print(traceback.format_exc())
        print("-------------------------------")


