import mysql.connector
from decouple import config
import os
import sc2reader as sc2
from sc2reader.objects import Player
from functions.stats import getMyTeamnumber, worker_counter2, logWorker
import traceback

def match_result(player, opponent)->str:

    race_1 = player.play_race
    race_2 = opponent.play_race
    result = player.result
    if race_1 == 'Zerg':
        if race_2 == 'Zerg':
            if result == 'Win':
                return 'z_z_win'
            elif result == 'Loss':
                return 'z_z_lose'
        elif race_2 == 'Terran':
            if result == 'Win':
                return 'z_t_win'
            elif result == 'Loss':
                return 'z_t_lose'
        elif race_2 == 'Protoss':
            if result == 'Win':
                return 'z_p_win'
            elif result == 'Loss':
                return 'z_p_lose'
    elif race_1 == 'Terran':
        if race_2 == 'Zerg':
            if result == 'Win':
                return 't_z_win'
            elif result == 'Loss':
                return 't_z_lose'
        elif race_2 == 'Terran':
            if result == 'Win':
                return 't_t_win'
            elif result == 'Loss':
                return 't_t_lose'
        elif race_2 == 'Protoss':
            if result == 'Win':
                return 't_p_win'
            elif result == 'Loss':
                return 't_p_lose'
    elif race_1 == 'Protoss':
        if race_2 == 'Zerg':
            if result == 'Win':
                return 'p_z_win'
            elif result == 'Loss':
                return 'p_z_lose'
        elif race_2 == 'Terran':
            if result == 'Win':
                return 'p_t_win'
            elif result == 'Loss':
                return 'p_t_lose'
        elif race_2 == 'Protoss':
            if result == 'Win':
                return 'p_p_win'
            elif result == 'Loss':
                return 'p_p_lose'

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
            continue

        replay = sc2.load_replay(path + f, load_map = False)
        # print(f)
        if replay.type == '1v1' and replay.frames > (sec * 22.404):

            opponent = replay.players[0]
            opponent_uid = opponent.detail_data['bnet']['uid']

            player = replay.players[1]
            player_uid = player.detail_data['bnet']['uid']

            if opponent_uid == 818362 or opponent_uid == 1931022:
                opponent = replay.players[1]
                opponent_uid = opponent.detail_data['bnet']['uid']

                player = replay.players[0]
                player_uid = player.detail_data['bnet']['uid']


            if not opponent.is_human :
                continue

            sql = f"SELECT * FROM match_results WHERE player_1 = {player_uid} AND player_2 = {opponent_uid}"
            mycursor.execute(sql, id)

            myresult = mycursor.fetchall()
            print(len(myresult))

            if len(myresult) == 0:
                column = (match_result(player, opponent))
                sql_insert = f"INSERT INTO match_results (player_1, player_2, {column}) VALUES ({player_uid},{opponent_uid}, 1)"
                mycursor.execute(sql_insert)
                mydb.commit()
                print("insert")
            else:
                column = match_result(player, opponent)
                sql_update = f"UPDATE match_results set {column} = {column} + 1 WHERE player_1 = {player_uid} AND player_2 = {opponent_uid}"
                mycursor.execute(sql_update)
                mydb.commit()
                print("update")


    except Exception as e:
        # raise e
        print("-------------------------------")
        print(traceback.format_exc())
        print("-------------------------------")


