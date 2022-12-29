import mysql.connector
import os
import sc2reader as sc2
import traceback
from decouple import config
from sc2reader.objects import Player

from parse_matches import update_db


password = config('MYSQL_PASSWORD')
user = config('USER_NAME')
path = 'C:/Users/loren/Documents/StarCraft II/Accounts/66185323/1-S2-2-818362/Replays/Multiplayer/'
path_2 = 'C:/Users/loren/Documents/StarCraft II/Accounts/66185323/1-S2-1-1931022/Replays/Multiplayer/'

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

sec = 1 # second you are interesed at

for f in files:
    update_db(mydb, mycursor, path + f)

for f in files_2:
    update_db(mydb, mycursor, path_2 + f)


