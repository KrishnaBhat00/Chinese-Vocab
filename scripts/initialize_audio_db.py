import sqlite3
import os
from sqlite3 import Error
import pandas as pd
import os


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"{sqlite3.sqlite_version=}")
        return conn
    except Error as e:
        print(e)
    return conn

def create_table(conn, statement):
    try:
        c = conn.cursor()
        c.execute(statement)
    except Error as e:
        print(e)

def createVocab(conn, vocab):
    statement = "INSERT INTO audio(name, pinyin, file, def, appearance, totalAsked, correct) VALUES(?,?,?,?,?,?,?)"
    c = conn.cursor()
    c.execute(statement, vocab)
    conn.commit()


def main():
    path = os.getcwd()
    database = os.path.join(path, "databases", "vocabs.db")
    if not os.path.exists(database): os.mkdir(os.path.join(os.getcwd(),"databases"))
    sql_create_vocabs = """ CREATE TABLE IF NOT EXISTS audio (
        id integer PRIMARY KEY,
        name text NOT NULL,
        pinyin text,
        file text,
        def text,
        appearance integer,
        totalAsked integer,
        correct integer
    );"""
    conn = create_connection(database)
    if conn is not None:
        create_table(conn, sql_create_vocabs)
    else:
        print("error, cannot connect to database")

    path = os.path.join(os.getcwd(), "static", "Chinese Vocab Community.xlsx")
    sheet = pd.read_excel(path, sheet_name='news audio')
    print (sheet)

    for row in sheet.iterrows():
        arr = []
        for i in range(len(row[1])):
            arr.append(row[1][i])
        vocab = (
            arr[0].strip("\t"),
            arr[1].strip("\t"),
            arr[2],
            arr[3],
            arr[4],
            0,
            0
        )
        createVocab(conn, vocab)

if __name__ == '__main__':
    main()