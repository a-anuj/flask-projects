from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import data_required
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:anuj2006@localhost/list_users'
app.config['SECRET_KEY'] = "mahi@1234"
db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Name %r>' % self.name


class UserForm(FlaskForm):
    name = StringField("Name", validators=[data_required()])
    email = StringField("Email", validators=[data_required()])
    submit = SubmitField("Submit")


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


@app.route('/name_form', methods=['GET', "POST"])
def name_for_form():
    name = None
    form = SimpleForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted Successfully")
    return render_template("name_form.html", name=name, form=form)


@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash("User added Successfully")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html", form=form, name=name, our_users=our_users)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
