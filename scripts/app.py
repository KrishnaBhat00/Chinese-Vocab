from Reader import vocabs
from flask import Flask, render_template, request

# if the name changes it should be run with --app
app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    shit = "sex"
    if request.method == 'POST':
        shit = "fuck"
        print(shit)
    return render_template('index.html', char=shit)

# @app.post('/')
# def index_post():
#     # determine what is needed and get it 
#     print(request.form)
#     return "shit"

if __name__ == '__main__':
    app.run(debug=True)