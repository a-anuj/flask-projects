from flask import Flask, render_template, flash, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from webforms import UserForm, PostForm, SimpleForm, PasswordForm, LoginForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:anuj2006@localhost/list_users'
app.config['SECRET_KEY'] = "mahi@1234"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
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


@app.route('/')
def index():
    learn_list = ["flask", "jinja2", "Flask Forms", "SQLAlchemy", "Werkzeug", "MySQL", "Migration"]
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
            user = Users(name=form.name.data,username=form.username.data, email=form.email.data, color=form.color.data,
                         password_hash=hashed_password)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.username.data = ''
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
@login_required
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


@app.route('/posts')
def Posts():
    all_posts = posts.query.order_by(posts.date_posted)
    return render_template('blog_posts.html', all_posts=all_posts)


@app.route('/posts/<int:id>')
def view_posts(id):
    view_post = posts.query.get_or_404(id)
    return render_template('spe_blog.html', view_post=view_post)


@app.route('/posts/edit/<int:id>', methods=['POST', 'GET'])
@login_required
def edit_post(id):
    form = PostForm()
    post = posts.query.get_or_404(id)
    if form.validate_on_submit():
        post.title = form.title.data
        post.author = form.author.data
        post.slug = form.slug.data
        post.content = form.content.data

        db.session.add(post)
        db.session.commit()
        flash("Blog Updated Successfully")
        redirect(url_for("view_posts", id=post.id))
    form.title.data = post.title
    form.content.data = post.content
    form.slug.data = post.slug
    form.author.data = post.author
    return render_template("edit_post.html", form=form)


@app.route('/delete/posts/<int:id>')
@login_required
def delete_post(id):
    post = posts.query.get_or_404(id)
    try:
        db.session.delete(post)
        db.session.commit()

        flash("Blog deleted successfully")

        all_posts = posts.query.order_by(posts.date_posted)
        return render_template('blog_posts.html', all_posts=all_posts)

    except:
        flash("Error Occurred")

        all_posts = posts.query.order_by(posts.date_posted)
        return render_template('blog_posts.html', all_posts=all_posts)


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


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash("Log in Successfull")
                return redirect(url_for('dashboard'))
            else:
                flash("Wrong Password")
        else:
            flash("User Not found")
    return render_template('login.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = UserForm()
    id = current_user.id
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.color = request.form['color']
        name_to_update.username = request.form['username']
        try:
            db.session.commit()
            flash("User Updated Successfully")
            return render_template("dashboard.html", form=form, name_to_update=name_to_update, id=id)
        except:
            flash("Error")
            return render_template("dashboard.html", form=form, name_to_update=name_to_update, id=id)

    else:
        return render_template("dashboard.html", form=form, name_to_update=name_to_update, id=id)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("Log out successfull")
    return redirect(url_for('login'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
