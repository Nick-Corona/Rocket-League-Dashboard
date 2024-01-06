#!/usr/bin/env python3

import pygsheets
import pandas as pd
import psycopg2
import os
import sys
import logging as log
from datetime import datetime

cur_date = datetime.today().strftime('%Y-%m-%d')

log.basicConfig(
        filename=f'{cur_date} run.log',
        level=log.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


def get_db_connection(*args):
    connection = None
    cursor = None
    try:
        connection = psycopg2.connect(database='postgres',
                                      user='postgres',
                                      password=os.environ['db_password'],
                                      host=os.environ['db_host'],
                                      port=5432)
    except Exception as e:
        print(e)
        return 'Error while trying to fetch the records'
    return connection


def get_max_gameid(schema):
    sql = f'select coalesce(max(gameid),0) from {schema}.mystats'
    maxid_connection = None

    try:
        maxid_connection = get_db_connection()
        if maxid_connection is not None:
            with maxid_connection.cursor() as cursor:
                cursor.execute(sql)
                return cursor.fetchone()[0]
    except Exception as e:
        print(e)
        return 'Error getting max gameid'
    finally:
        if maxid_connection is not None:
            maxid_connection.close()

def get_google_sheet(gameid, tab):
    spreadsheetid = '17Jwl9XNratzqjvprgJIRa2BG5OEm5ZODtOAMPhQuWlo'

    #client = pygsheets.authorize(client_secret = "credentials.json")
    client = pygsheets.authorize(service_file='service_account_keys.json')

    spreadsheet = client.open_by_key(spreadsheetid)
    worksheet = spreadsheet.worksheet_by_title(tab)

    fromgameid = str(gameid + 1)
    togameid = str(len(worksheet.get_all_values(include_tailing_empty_rows=False, include_tailing_empty=False)))

    if fromgameid == togameid:
        return 'No new games added'
    elif fromgameid > togameid:
        #raise ValueError(f"ERROR: More games in database: {fromgameid} than Google Sheet: {togameid}")
        return f'ERROR: More games in database: {fromgameid} than Google Sheet: {togameid}'

    if tab == '1v1':
        column = 'K'
    elif tab == '2v2':
        column = 'V'
    elif tab == '3v3':
        column = 'AF'

    try:
        statsheet = worksheet.get_values(start=f'A{fromgameid}', end=f'{column}{togameid}', include_tailing_empty_rows=False, include_tailing_empty=False, returnas='matrix')
    except Exception as e:
        return e

    return statsheet


def db_insert(statsheet, schema):
    stats_df = pd.DataFrame(statsheet)
    stats_df.columns = stats_df.iloc[0]
    stats_df = stats_df[1:]
    #stats_df = stats_df.iloc[:,20:22].replace([None, 'None'], 'null', inplace=True)

    mystats_sql = f'insert into {schema}.mystats (score, goals, assists, saves, shots) values (%s, %s, %s, %s, %s)'
    teammate1_sql = f'insert into {schema}.teammate1 (score, goals, assists, saves, shots) values (%s, %s, %s, %s, %s)'
    teammate2_sql = f'insert into {schema}.teammate2 (score, goals, assists, saves, shots) values (%s, %s, %s, %s, %s)'
    opponent1_sql = f'insert into {schema}.opponent1 (score, goals, assists, saves, shots) values (%s, %s, %s, %s, %s)'
    opponent2_sql = f'insert into {schema}.opponent2 (score, goals, assists, saves, shots) values (%s, %s, %s, %s, %s)'
    opponent3_sql = f'insert into {schema}.opponent3 (score, goals, assists, saves, shots) values (%s, %s, %s, %s, %s)'
    gamedetails_sql = f"""insert into {schema}.gamedetails (overtime, comms) values (%s, %s)"""

    mystats_tuple = tuple(stats_df.iloc[:, 0:5].itertuples(index=False, name=None))

    if schema == 'solo':

        gamedetails_sql = f'insert into {schema}.gamedetails (overtime) values (%s)'

        opponent1_tuple = tuple(stats_df.iloc[:, 5:10].itertuples(index=False, name=None))
        gamedetails_tuple = tuple(stats_df.iloc[:, 10:11].itertuples(index=False, name=None))

        try:
            insert_connection = get_db_connection()
            if insert_connection is not None:
                with insert_connection.cursor() as cursor:
                    for game in range(len(mystats_tuple)):
                        cursor.execute(mystats_sql % mystats_tuple[game])
                    print(f'{game + 1} mystats {schema} games inserted')

                    for game in range(len(opponent1_tuple)):
                        cursor.execute(opponent1_sql % opponent1_tuple[game])
                    print(f'{game + 1} opponent1 {schema} games inserted')

        except Exception as e:
            print(e)
            return 'Error getting max gameid'
        finally:
            if insert_connection is not None:
                insert_connection.commit()
                insert_connection.close()

    elif schema == 'doubles':

        teammate1_tuple = tuple(stats_df.iloc[:, 5:10].itertuples(index=False, name=None))
        opponent1_tuple = tuple(stats_df.iloc[:, 10:15].itertuples(index=False, name=None))
        opponent2_tuple = tuple(stats_df.iloc[:, 15:20].itertuples(index=False, name=None))
        gamedetails_clean = stats_df.iloc[:, 20:22].copy()
        gamedetails_clean['Overtime'].replace([None, 'None', ''], 'null', inplace=True)
        gamedetails_clean['Comms'].replace([None, 'None', ''], 'Solo queue', inplace=True)
        gamedetails_tuple = tuple(gamedetails_clean.itertuples(index=False, name=None))

        try:
            insert_connection = get_db_connection()
            if insert_connection is not None:
                with insert_connection.cursor() as cursor:
                    for game in range(len(mystats_tuple)):
                        cursor.execute(mystats_sql % mystats_tuple[game])
                    print(f'{game + 1} mystats {schema} games inserted')

                    for game in range(len(teammate1_tuple)):
                        cursor.execute(teammate1_sql % teammate1_tuple[game])
                    print(f'{game + 1} teammate1 {schema} games inserted')

                    for game in range(len(opponent1_tuple)):
                        cursor.execute(opponent1_sql % opponent1_tuple[game])
                    print(f'{game + 1} opponent1 {schema} games inserted')

                    for game in range(len(opponent2_tuple)):
                        cursor.execute(opponent2_sql % opponent2_tuple[game])
                    print(f'{game + 1} opponent2 {schema} games inserted')

                    for game in range(len(gamedetails_tuple)):
                        cursor.execute(gamedetails_sql % gamedetails_tuple[game])
                    print(f'{game + 1} {schema} gamedetails inserted')

        except Exception as e:
            print(e)
            return 'Error getting max gameid'
        finally:
            if insert_connection is not None:
                insert_connection.commit()
                insert_connection.close()

    elif schema == 'trios':

        teammate1_tuple = tuple(stats_df.iloc[:, 5:10].itertuples(index=False, name=None))
        teammate2_tuple = tuple(stats_df.iloc[:, 10:15].itertuples(index=False, name=None))
        opponent1_tuple = tuple(stats_df.iloc[:, 15:20].itertuples(index=False, name=None))
        opponent2_tuple = tuple(stats_df.iloc[:, 20:25].itertuples(index=False, name=None))
        opponent3_tuple = tuple(stats_df.iloc[:, 25:30].itertuples(index=False, name=None))
        gamedetails_tuple = tuple(stats_df.iloc[:, 30:32].itertuples(index=False, name=None)) # refer back to doubles. sumn wrong
        gamedetails_clean = stats_df.iloc[:, 30:32].copy()
        gamedetails_clean.replace([None, 'None', ''], 'Solo queue', inplace=True)
        gamedetails_tuple = tuple(gamedetails_clean.itertuples(index=False, name=None))

        try:
            insert_connection = get_db_connection()
            if insert_connection is not None:
                with insert_connection.cursor() as cursor:
                    for game in range(len(mystats_tuple)):
                        cursor.execute(mystats_sql % mystats_tuple[game])
                    print(f'{game + 1} mystats {schema} games inserted')

                    for game in range(len(teammate1_tuple)):
                        cursor.execute(teammate1_sql % teammate1_tuple[game])
                    print(f'{game + 1} teammate1 {schema} games inserted')

                    for game in range(len(teammate2_tuple)):
                        cursor.execute(teammate2_sql % teammate2_tuple[game])
                    print(f'{game + 1} teammate2 {schema} games inserted')

                    for game in range(len(opponent1_tuple)):
                        cursor.execute(opponent1_sql % opponent1_tuple[game])
                    print(f'{game + 1} opponent1 {schema} games inserted')

                    for game in range(len(opponent2_tuple)):
                        cursor.execute(opponent2_sql % opponent2_tuple[game])
                    print(f'{game + 1} opponent2 {schema} games inserted')

                    for game in range(len(opponent3_tuple)):
                        cursor.execute(opponent3_sql % opponent3_tuple[game])
                    print(f'{game + 1} opponent3 {schema} games inserted')

                    for game in range(len(gamedetails_tuple)):
                        cursor.execute(gamedetails_sql % gamedetails_tuple[game], )
                    print(f'{game + 1} {schema} gamedetails inserted')

        except Exception as e:
            print(e)
            return 'Error getting max gameid'
        finally:
            if insert_connection is not None:
                insert_connection.commit()
                insert_connection.close()


def main(args):
    tab = None
    schema = None

    if args == '1':
        tab = '1v1'
        schema = 'solo'
    elif args == '2':
        tab = '2v2'
        schema = 'doubles'
    elif args == '3':
        tab = '3v3'
        schema = 'trios'
    else:
        print(f'Invalid argument: {str(args)} expected 1,2,3')

    last_db_game = get_max_gameid(schema)
    google_sheet = get_google_sheet(last_db_game, tab)

    if isinstance(google_sheet, str):
        print(google_sheet)
    else:
        db_insert(google_sheet, schema)


if __name__ == '__main__':
    main(sys.argv[1])
