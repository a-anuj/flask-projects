from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/name/<username>')
def findName(username):
    return "Hello {}".format(username)


app.run(debug=True)
