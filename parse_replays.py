import mysql.connector
import os
import sc2reader as sc2
import traceback
from decouple import config
from sc2reader.objects import Player
from functions.stats import analize_drone_kills, copy_replay, worker_timeline

from parse_matches import update_db, update_replay
import os

password = config('MYSQL_PASSWORD')
user = config('USER_NAME')
path = config('REPLAY_FOLDER_2', default='')
path_2 = config('REPLAY_FOLDER', default='')
save_path = config('ANALYSIS_FOLDER', default='')

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
files_2 = os.listdir(path_2)
files_3 = os.listdir(save_path)

get_replays_sql = f"SELECT path FROM trainer.replay_table where player_2 = 6556840 and \
    (player_1 = 1931022 or player_1 = 818362) and race_1 = 'Zerg' and race_2 = 'Terran' and result = 'Loss';"

# SELECT * FROM trainer.replay_table where file_hash like '%a4b37353e7';

mycursor.execute(get_replays_sql)
myresult = mycursor.fetchall()

for f in files_3:
    # replay = sc2.load_replay(f[0], load_map = False)
    replay = sc2.load_replay(save_path + f, load_map = False)
    worker_timeline(replay)

for f in myresult:
    replay = sc2.load_replay(f[0], load_map = False)
    worker_timeline(replay)
    # break
    # copy_replay(f[0], replay, save_path)
    # analize_drone_kills(replay, 6556840)

exit()


for f in files:
    update_db(mydb, mycursor, path + f)

for f in files_2:
    update_db(mydb, mycursor, path_2 + f)


