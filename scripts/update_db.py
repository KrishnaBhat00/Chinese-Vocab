import sqlite3
from sqlite3 import Error
from Reader import vocabs
import os

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"{sqlite3.sqlite_version=}")
        return conn
    except Error as e:
        print(e)
    return conn

def check_same(conn, i):
    try:
        if i <= 0: # throw exception
            raise Exception("Exception: index less than 0")
    except Exception as e:
        print(e)
    cur = conn.cursor()
    count = int(cur.execute("SELECT Count(*) FROM vocabs").fetchone()[0])
    if i <= count:
        try: 
            sql = "SELECT * FROM vocabs WHERE id=?"
            row = cur.execute(sql, (i, )).fetchone()
            if vocabs[i - 1].getChars() != row[1]:
                raise Exception("Exception: Mismatch between xlsx file and database")
        except Exception as e:
            print (e)
    else:
        sql = "INSERT INTO vocabs(chars, pinyin, def, totalAsked, correct) VALUES(?,?,?,?,?)"
        vocab = (vocabs[i - 1].getChars(), vocabs[i - 1].getPinyin(), vocabs[i - 1].getDefin(), 0, 0)
        cur.execute(sql, vocab)
        print (cur.lastrowid)   
        conn.commit()

def main():
    path = os.getcwd()
    database = path + r"\databases\vocabs.db" if platform.system() == 'Windows' else path + r"/databases/vocabs.db"
    conn = create_connection(database)
    for i in vocabs:
        check_same(conn, i + 1)
if __name__ == "__main__":
    main()