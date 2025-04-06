import sqlite3
from sqlite3 import Error
import os
import pandas as pd

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"{sqlite3.sqlite_version=}")
        return conn
    except Error as e:
        print(e)
    return conn

def check_same(conn, i, vocab):
    try:
        if i <= 0: # throw exception
            raise Exception("Exception: index less than 0")
    except Exception as e:
        print(e)
    cur = conn.cursor()
    count = int(cur.execute("SELECT Count(*) FROM audio").fetchone()[0])
    if i <= count:
        try: 
            sql = "SELECT * FROM audio WHERE id=?"
            row = cur.execute(sql, (i, )).fetchone()
            if vocab[0] != row[1]:
                raise Exception("Exception: Mismatch between xlsx file and database")
        except Exception as e:
            print (e)
    else:
        sql = "INSERT INTO audio(name, pinyin, file, def, appearance, totalAsked, correct) VALUES(?,?,?,?,?,?,?)"
        cur.execute(sql, vocab)
        print (cur.lastrowid)
        conn.commit()

def main():
    path = os.getcwd()
    database = os.path.join(path, "databases", "vocabs.db")
    conn = create_connection(database)
    path = os.path.join(os.getcwd(), "static", "Chinese Vocab Community.xlsx")
    sheet = pd.read_excel(path, sheet_name='news audio')
    print (sheet)

    j = 1
    for row in sheet.iterrows():
        arr = []
        for i in range(len(row[1])):
            arr.append(row[1][i])
        vocab = (
            arr[0].strip("\t"),
            arr[1].strip("\t"),
            arr[2].strip("\t"),
            arr[3],
            arr[4],
            0,
            0
        )
        check_same(conn, j, vocab)
        j += 1

if __name__ == "__main__":
    main()