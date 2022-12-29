import mysql.connector
import os
import sc2reader as sc2
import traceback
from decouple import config
from sc2reader.objects import Player

def insert_player(db_connection, db_cursor, player):
    tag2 = "-"
    if player.clan_tag != "":
        tag = bytes(player.clan_tag, 'utf-8')
        tag2 = bytes.decode(tag,'utf-8')

    sql = f"INSERT INTO player_table (uid, player_name, clan_tag, region, subregion, player_url) VALUES ({uid}, {player.name}, {tag2}, {player.region}, {player.subregion}, {player.url})"
    val = (uid, player.name, tag2, player.region, player.subregion, player.url)

    db_cursor.execute(sql, val)
    db_connection.commit()

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
sec = 1 # second you are interesed at

for f in files:
    try:
        if ".writeCacheBackup" in f:
            print("not a replay file")
            continue # skip

        replay = sc2.load_replay(path + f, load_map = False)

        if replay.type != '1v1' or replay.frames < (sec * 22.404):
            continue # skip

        p = replay.players[0]
        uid = p.detail_data['bnet']['uid']
        if uid == 818362 or uid == 1931022: # my ids
            p = replay.players[1]
            uid = p.detail_data['bnet']['uid']
        if not p.is_human or uid == 6556840 or uid == 6795698 or uid == 5009518: # Lobo y Kinesin y Stati
            continue # skip

        insert_player(mydb, mycursor, p)

    except Exception as e:
        # raise e
        print("-------------------------------")
        # print(traceback.format_exc())
        print(f,e)
        print("-------------------------------")


