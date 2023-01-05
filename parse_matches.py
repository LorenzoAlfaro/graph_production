import mysql.connector
import os
import sc2reader as sc2
import traceback
from decouple import config
from sc2reader.objects import Player


def insert_player(db_connection, db_cursor, player, replay):
    sql = f"SELECT * FROM replay_table WHERE file_hash = '{replay.filehash}'"
    db_cursor.execute(sql)
    myresult = db_cursor.fetchall()
    if myresult[0][1] == 1:
        return # it has been already updated

    uid = player.detail_data['bnet']['uid']
    tag2 = "-"
    if player.clan_tag != "":
        tag = bytes(player.clan_tag, 'utf-8')
        tag2 = bytes.decode(tag,'utf-8')

    sql = f"INSERT INTO player_table (uid, player_name, clan_tag, region, subregion, player_url) VALUES (\
        {uid}, '{player.name}', '{tag2}', '{player.region}', {player.subregion}, '{player.url}')"
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

def update_match_record(db_connection, db_cursor, player, opponent, replay):
    sql = f"SELECT * FROM replay_table WHERE file_hash = '{replay.filehash}'"
    db_cursor.execute(sql)
    myresult = db_cursor.fetchall()
    if myresult[0][2] == 1:
        return # it has been already updated

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

def register_replay(db_connection, db_cursor, player, opponent, replay, player_updated:int, match_updated:int):
    opponent_uid = opponent.detail_data['bnet']['uid']
    player_uid = player.detail_data['bnet']['uid']
    sql = f"SELECT * FROM replay_table WHERE file_hash = '{replay.filehash}'"
    db_cursor.execute(sql)
    myresult = db_cursor.fetchall()

    if len(myresult) == 0:
        sql_insert = f"INSERT INTO replay_table\
            (file_hash, player_updated, match_updated, path, player_1, player_2, race_1, race_2, result, map_name, frames)\
            VALUES ('{replay.filehash}', {player_updated}, {match_updated}, '{replay.filename}', {player_uid}, {opponent_uid}, '{player.play_race}', '{opponent.play_race}',\
            '{player.result}', '{replay.map_name}', {replay.frames})"
        # print(sql_insert)
        db_cursor.execute(sql_insert)
        db_connection.commit()

def update_db(mydb, mycursor, file_path):
    player_updated = 0
    match_updated = 0
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

        insert_player(mydb, mycursor, opponent, replay)
        player_updated = 1
        print("player created", file_path)
    except Exception as e:
        # raise e
        print("----------PLAYER TABLE ERROR------------------")
        print(traceback.format_exc())
        print(e, file_path)
        print("-------------------------------")

    try:
        update_match_record(mydb, mycursor, player, opponent, replay)
        match_updated = 1
        print("match updated", file_path)
    except Exception as e:
        # raise e
        print("----------MATCH TABLE ERROR-------------------")
        print(traceback.format_exc())
        print(e, file_path)
        print("-------------------------------")

    try:
        register_replay(mydb, mycursor, player, opponent, replay, player_updated, match_updated)
        print("replay created", file_path)
    except Exception as e:
        # raise e
        print("-----------REPLAY TABLE ERROR-------------")
        print(traceback.format_exc())
        print(e, file_path)
        print("-------------------------------")

def update_replay(mydb, mycursor, file_path:str):
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

        register_replay(mydb, mycursor, player, opponent, replay)
    except Exception as e:
        # raise e
        print("-------------------------------")
        print(traceback.format_exc())
        print(e, file_path)
        print("-------------------------------")
