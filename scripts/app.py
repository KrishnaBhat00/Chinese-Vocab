import sqlite3
from sqlite3 import Error
import json
from flask import Flask, render_template, request
import random

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

def updateUsage(form, cur):
    if form['success'] != 'null':
        update = """UPDATE vocabs SET totalAsked = ?, correct = ? WHERE id=?"""
        currentInfo = "SELECT * FROM vocabs WHERE id=?"
        output = cur.execute(currentInfo, (form['id'], )).fetchone()
        total = int(output[4])
        correct = int(output[5])
        total += 1
        if form['success'] == 'yes':
            correct += 1
            cur.execute(update, (total, correct, form['id']))
        if form['success'] == 'no':
            cur.execute(update, (total, correct, form['id']))
        conn.commit()


def nextFlashcard(form):
    cur = conn.cursor()
    count = cur.execute("SELECT Count(*) FROM vocabs").fetchone()[0]
    statement = "SELECT * FROM vocabs WHERE id=?"
    output = ""
    if not form["id"] or not (not form["answer"]):
        updateUsage(form, cur)
        id = random.randint(1, count)
        output = cur.execute(statement, (id,)).fetchone()
        json_data = json.dumps({"id":id, "char":output[1], "answer":""})
    else:
        id = form['id']
        output = cur.execute(statement, (id,)).fetchone()
        answer = f"{output[2]}\n{output[3]}"
        json_data = json.dumps({"id":id, "char":form["char"],"answer":answer})
    return json_data



@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route("/flashcard", methods=['GET', 'POST'])
def flashcard():
    print(request.form)
    if (request.method == 'POST'):
        return nextFlashcard(request.form)
    else:
        return render_template('flashcard.html')

if __name__ == '__main__':
    app.run(debug=True)