import mysql.connector
import os
import sc2reader as sc2
import traceback
from decouple import config
from sc2reader.objects import Player


def insert_player(db_connection, db_cursor, player):
    uid = player.detail_data['bnet']['uid']
    tag2 = "-"
    if player.clan_tag != "":
        tag = bytes(player.clan_tag, 'utf-8')
        tag2 = bytes.decode(tag,'utf-8')

    sql = f"INSERT INTO player_table (uid, player_name, clan_tag, region, subregion, player_url) VALUES ({uid}, '{player.name}', '{tag2}', '{player.region}', {player.subregion}, '{player.url}')"
    db_cursor.execute(sql)
    db_connection.commit()

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

def update_match_record(db_connection, db_cursor, player, opponent):
    print(player.name,player.play_race, opponent.name,opponent.play_race, player.result)
    opponent_uid = opponent.detail_data['bnet']['uid']
    player_uid = player.detail_data['bnet']['uid']
    sql = f"SELECT * FROM match_results WHERE player_1 = {player_uid} AND player_2 = {opponent_uid}"
    db_cursor.execute(sql)
    myresult = db_cursor.fetchall()

    if len(myresult) == 0:
        column = match_result(player, opponent)
        sql_insert = f"INSERT INTO match_results (player_1, player_2, {column}) VALUES ({player_uid},{opponent_uid}, 1)"
        db_cursor.execute(sql_insert)
        db_connection.commit()
    else:
        id = myresult[0][0]
        column = match_result(player, opponent)
        sql_update = f"UPDATE match_results set {column} = {column} + 1 WHERE id = {id}"
        db_cursor.execute(sql_update)
        db_connection.commit()


def update_db(mydb, mycursor, file_path):
    try:
        sec = 1
        if ".writeCacheBackup" in file_path:
            print("not a replay file")
            return
        replay = sc2.load_replay(file_path, load_map = False)
        # print(f)
        if replay.type != '1v1' or replay.frames < (sec * 22.404):
            return

        opponent = replay.players[0]
        player = replay.players[1]
        opp_uid = opponent.detail_data['bnet']['uid']

        if opp_uid == 818362 or opp_uid == 1931022:
            opponent = replay.players[1]
            player = replay.players[0]

        if not opponent.is_human :
            return

        insert_player(mydb, mycursor, opponent)
    except Exception as e:
        # raise e
        print("-------------------------------")
        # print(traceback.format_exc())
        print(e, file_path)
        print("-------------------------------")

    try:
        update_match_record(mydb, mycursor, player, opponent)
    except Exception as e:
        # raise e
        print("-------------------------------")
        # print(traceback.format_exc())
        print(e, file_path)
        print("-------------------------------")
