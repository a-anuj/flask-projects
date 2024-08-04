from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import data_required

app = Flask(__name__)
app.config['SECRET_KEY'] = "mahi@1234"


class SimpleForm(FlaskForm):
    name = StringField("What's your name", validators=[data_required()])
    submit = SubmitField("Submit")


@app.route('/')
def index():
    learn_list = ["flask", "jinja2"]
    return render_template("index.html", learn_list=learn_list)


@app.route('/name/<username>')
def findName(username):
    return render_template("name.html", username=username)


@app.errorhandler(404)
def pageNotFound(e):
    return render_template("404.html"), 404


@app.route('/name_form', methods = ['GET', "POST"])
def name_for_form():
    name = None
    form = SimpleForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template("name_form.html", name=name, form=form)


app.run(debug=True)
