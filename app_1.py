from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import data_required, EqualTo
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from wtforms.widgets import TextArea

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:anuj2006@localhost/list_users'
app.config['SECRET_KEY'] = "mahi@1234"
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    color = db.Column(db.String(120))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    password_hash = db.Column(db.String(200))


class posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    author = db.Column(db.String(255))
    slug = db.Column(db.String(255))
    content = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow())

    @property
    def password(self):
        raise AttributeError("Password cannot be viewed")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Name %r>' % self.name


class UserForm(FlaskForm):
    name = StringField("Name", validators=[data_required()])
    email = StringField("Email", validators=[data_required()])
    color = StringField("Favorite color")
    submit = SubmitField("Submit")
    password_hash = PasswordField("Password", validators=[data_required(), EqualTo('password_hash2')])
    password_hash2 = PasswordField("Confirm Password", validators=[data_required()])


class SimpleForm(FlaskForm):
    name = StringField("What's your name", validators=[data_required()])
    submit = SubmitField("Submit")


class PasswordForm(FlaskForm):
    email = StringField("What's your email", validators=[data_required()])
    password_hash = PasswordField("What's your password", validators=[data_required()])
    submit = SubmitField("Submit")


class PostForm(FlaskForm):
    title = StringField("Title", validators=[data_required()])
    content = StringField("Content", validators=[data_required()], widget=TextArea())
    author = StringField("Author", validators=[data_required()])
    slug = StringField("Slug", validators=[data_required()])
    submit = SubmitField("Submit", validators=[data_required()])


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
            hashed_password = generate_password_hash(form.password_hash.data)
            user = Users(name=form.name.data, email=form.email.data, color=form.color.data,
                         password_hash=hashed_password)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.color.data = ''
        form.password_hash.data = ''
        flash("User added Successfully")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html", form=form, name=name, our_users=our_users)


@app.route('/delete/<int:id>')
def delete(id):
    form = UserForm()
    name = None
    name_to_delete = Users.query.get_or_404(id)
    try:
        db.session.delete(name_to_delete)
        db.session.commit()
        flash("User updated successfully")
        our_users = Users.query.order_by(Users.date_added)
        return render_template("add_user.html", form=form, name=name, our_users=our_users)
    except:
        flash("Error Occurred!")
        our_users = Users.query.order_by(Users.date_added)
        return render_template("add_user.html", form=form, name=name, our_users=our_users)


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.color = request.form['color']
        try:
            db.session.commit()
            flash("User Updated Successfully")
            return render_template("update.html", form=form, name_to_update=name_to_update, id=id)
        except:
            flash("Error")
            return render_template("update.html", form=form, name_to_update=name_to_update, id=id)

    else:
        return render_template("update.html", form=form, name_to_update=name_to_update, id=id)


@app.route('/date')
def return_date():
    return {"Date": date.today()}


@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        post = posts(title=form.title.data, content=form.content.data, author=form.author.data, slug=form.slug.data)
        form.title.data = ''
        form.author.data = ''
        form.content.data = ''
        form.slug.data = ''

        db.session.add(post)
        db.session.commit()

        flash("Blog Post submitted successfully!")
    return render_template("add_post.html", form=form)


@app.route('/test_pw', methods=['GET', "POST"])
def test_pw():
    email = None
    password = None
    pw_to_check = None
    passed = None

    form = PasswordForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data
        value = form.password_hash.data
        form.email.data = ''
        form.password_hash.data = ''
        pw_to_check = Users.query.filter_by(email=email).first()
        passed = check_password_hash(pw_to_check.password_hash, password)
    return render_template("test_pw.html",
                           email=email,
                           password=password,
                           form=form,
                           pw_to_check=pw_to_check,
                           passed=passed
                           )


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
