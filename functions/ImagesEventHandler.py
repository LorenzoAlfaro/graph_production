import mysql.connector
from watchdog.events import RegexMatchingEventHandler
from decouple import config
import os
import sc2reader as sc2
import time

from parse_matches import update_db

class ImagesEventHandler(RegexMatchingEventHandler):

    def __init__(self):
        super().__init__()

    def on_created(self, event):
        filename, ext = os.path.splitext(event.src_path)
        print(f"created {filename}{ext}")
        time.sleep(1)
        self.new_replay(filename + ext)

    def new_replay(self, fileName):

        password = config('MYSQL_PASSWORD')
        user = config('USER_NAME')
        mydb = mysql.connector.connect(
            host="localhost",
            user=user,
            password=password,
            database="trainer",
            ssl_disabled=True
            )
        mycursor = mydb.cursor()

        update_db(mydb, mycursor, fileName)