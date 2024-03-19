from Reader import vocabs
from flask import Flask, render_template, request

# if the name changes it should be run with --app
app = Flask(__name__,template_folder='..\\templates',static_folder='..\\static')

@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route("/flashcard", methods=['POST'])
def flashcard():
    print(request.form)
    ret = ""
    if request.form["char"] == "":
        ret = "我"
    else: 
        ret = "我: I/me"
    return ret

if __name__ == '__main__':
    app.run(debug=True)