import sqlite3
from sqlite3 import Error
import json
from flask import Flask, render_template, request
import random
import os
import platform
import bleach

# if the name changes it should be run with --app

path = os.getcwd()
templates = os.path.join(path, "templates")
static = os.path.join(path, "static")
app = Flask(__name__,template_folder=templates,static_folder=static)

database = os.path.join(path, "databases", "vocabs.db")

def create_connection(db_file):
    # create a database connection to a SQLite database
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
    print(form)
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
        #char = bleach.clean(form['char'])
        char = output[1]
        answer = f"Pinyin: {output[2]}<br>Definition: {output[3]}"
        json_data = json.dumps({"id":id, "char":char,"answer":answer})
    return json_data

def nextReader(form, count):
    cur = conn.cursor()
    total = cur.execute("SELECT Count(*) FROM vocabs").fetchone()[0]
    statement = "SELECT * FROM vocabs WHERE id=?"
    output = ""
    if not form["id"] or not (not form["answer"]):
        updateUsage(form, cur)
        if not form['id']: currId = count
        elif int(form['id']) + 1 > total: currId = 0
        else: currId = int(form['id'])
        id = currId + 1
        output = cur.execute(statement, (id,)).fetchone()
        json_data = json.dumps({"id":id, "char":output[1], "answer":""})
    else:
        id = form['id']
        output = cur.execute(statement, (id,)).fetchone()
        char = output[1]
        answer = f"{output[2]}\n{output[3]}"
        json_data = json.dumps({"id":id, "char":char,"answer":answer})
    return json_data

def analyticsBase():
    cur = conn.cursor()
    statement = "SELECT * FROM vocabs"
    output = cur.execute(statement).fetchall()
    arr = []
    for row in output:
        if row[4] > 0: correctPer = f"{(row[5]/row[4] * 100):.1f}%"
        else: correctPer = 'N/A'
        result = {
            'ID': row[0],
            'Char': row[1],
            'PinYin': row[2],
            'Definition': row[3],
            'Appearances': row[4],
            'Correct': correctPer
        }
        arr.append(result)
    print (arr[1])
    json_data = json.dumps({"rows":arr})
    return json_data

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route("/flashcard", methods=['GET', 'POST'])
def flashcard():
    if (request.method == 'POST'):
        return nextFlashcard(request.form)
    else:
        return render_template('flashcard.html')

@app.route("/reader", methods=['GET', 'POST'])
def reader():
    count = 0
    if request.args.get('count') is not None: count = request.args.get('count')
    if (request.method == 'POST'):
        return nextReader(request.form, int(count))
    else:
        return render_template('reader.html')

@app.route("/analytics", methods=['GET','POST'])
def analytics():
    if (request.method == 'POST'):
        return analyticsBase()
    else: return render_template('data.html')


if __name__ == '__main__':
    app.run(debug=True)