import sqlite3
import os
from sqlite3 import Error
from Reader import vocabs

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
    statement = "INSERT INTO vocabs(chars, pinyin, def, totalAsked, correct) VALUES(?,?,?,?,?)"
    c = conn.cursor()
    c.execute(statement, vocab)
    conn.commit()


def main():
    path = os.getcwd()
    database = os.path.join(path, "databases", "vocabs.db")
    if not os.path.exists(database): os.mkdir(os.path.join(os.getcwd(),"databases"))
    sql_create_vocabs = """ CREATE TABLE IF NOT EXISTS vocabs (
        id integer PRIMARY KEY,
        chars text NOT NULL,
        pinyin text,
        def text,
        totalAsked integer,
        correct integer
    );"""
    conn = create_connection(database)
    # if conn is not None:
    #     create_table(conn, sql_create_vocabs)
    # else:
    #     print("error, cannot connect to database")

    # for i in vocabs:
    #     vocab = (vocabs[i].getChars(), vocabs[i].getPinyin(), vocabs[i].getDefin(), 0, 0)
    #     createVocab(conn, vocab)

if __name__ == '__main__':
    main()