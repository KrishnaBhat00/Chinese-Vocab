import sqlite3
from sqlite3 import Error
import json
from flask import Flask, render_template, request

# if the name changes it should be run with --app
app = Flask(__name__,template_folder='..\\templates',static_folder='..\\static')

database = r"C:\Users\aweso\Documents\Chinese Vocab\databases\vocabs.db"

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file, check_same_thread=False)
        return conn
    except Error as e:
        print(e)
    return conn

conn = create_connection(database)


def getNext(form):
    cur = conn.cursor()
    statement = "SELECT * FROM vocabs WHERE id=?"
    output = ""
    if not form["id"] or not (not form["answer"]):
        id = 4
        output = cur.execute(statement, (4,)).fetchone()[1]
        json_data = json.dumps({"id":id, "char":output[1], "answer":""})
    else: 
        id = 4
        output = cur.execute(statement, (form['id'],)).fetchone()
        answer = f"{output[2]}\t{output[3]}"
        json_data = json.dumps({"id":id, "char":form["char"],"answer":answer})
    return json_data



@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route("/flashcard", methods=['POST'])
def flashcard():
    print(request.form)
    c = conn.cursor()
    statement = "SELECT * FROM vocabs WHERE id=?"
    output = ""
    id = 0
    return getNext(request.form)

if __name__ == '__main__':
    app.run(debug=True)