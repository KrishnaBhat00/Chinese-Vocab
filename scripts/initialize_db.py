import sqlite3
from sqlite3 import Error
from Reader import vocabs

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.sqlite_version)
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
    statement = f"INSERT INTO vocabs(chars, pinyin, def) VALUES(?,?,?)"
    c = conn.cursor()
    c.execute(statement, vocab)
    conn.commit()


def main():
    database = r"C:\Users\aweso\Documents\Chinese Vocab\databases\vocabs.db"
    sql_create_vocabs = """ CREATE TABLE IF NOT EXISTS vocabs (
        id integer PRIMARY KEY,x
        chars text NOT NULL,
        pinyin text,
        def text
    );"""
    conn = create_connection(database)
    if conn is not None:
        create_table(conn, sql_create_vocabs)
    else:
        print("error, cannot connect to database")

    for i in vocabs:
        vocab = (vocabs[i].getChars(), vocabs[i].getPinyin(), vocabs[i].getDefin())
        createVocab(conn, vocab)

if __name__ == '__main__':
    main()