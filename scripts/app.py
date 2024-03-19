from Reader import vocabs
from flask import Flask, render_template, request

# if the name changes it should be run with --app
app = Flask(__name__,template_folder='..\\templates',static_folder='..\\static')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route("/flashcard", methods=['POST'])
def flashcard():
    print(request.form)
    output = ""
    if not request.form["char"]:
        output = "我"
    else: 
        output = "我: I/me"
    return output

if __name__ == '__main__':
    app.run(debug=True)