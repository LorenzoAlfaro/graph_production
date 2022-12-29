import mysql.connector
from decouple import config
import os
import sc2reader as sc2
from sc2reader.objects import Player
from functions.stats import getMyTeamnumber, worker_counter2, logWorker
import traceback

def match_result(player_1, player_2):

    race_1 = player_1.play_race
    race_2 = player_2.play_race
    result = player_1.result

    print(race_1,race_2,result)

    ...

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

            match_result(player, opponent)
            sql = "SELECT * FROM match_results WHERE player_2 = %s"
            id = (opponent_uid,)
            mycursor.execute(sql, id)
            print(opponent_uid)

            myresult = mycursor.fetchall()
            print(len(myresult))

            # if len(myresult==0):
            #     sql_insert = "INSERT INTO match_results (player_1, player_2, clan_tag, region, subregion, player_url) VALUES (%s, %s, %s, %s, %s, %s)"


            # print(p.name, p.result)
    except Exception as e:
        # raise e
        print("-------------------------------")
        print(traceback.format_exc())
        print("-------------------------------")


