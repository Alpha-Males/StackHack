"""


"""


import datetime
import os
import secrets


from flask import render_template, flash, url_for, redirect, request
from flask_login import login_user, current_user, login_required, logout_user
from PIL import Image


from todo import app, db, bcrypt
from todo.model import User, Todo, Tasks
from todo.forms import RegistrationForm, LoginForm


allowed_extensions = ["jpg", "png", "ppm"]


@app.route("/")
def home():
    """
    page for login and signup
    """
    return render_template("home.html")


def save_and_upload(file):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(file.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, "static/profile_pics", picture_fn)
    output_size = (125, 125)
    i = Image.open(file)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    pro_pic = url_for("static", filename="profile_pics/"
         + current_user.image_file)
    if request.method == "POST":
        file = request.files.get("file")
        picture_file = save_and_upload(file)
        current_user.image_file = picture_file
        db.session.commit()
        return redirect(url_for("account"))
    return render_template("account.html", pro_pic=pro_pic)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    print(form.validate_on_submit())

    if request.method == "POST":
        print(form.email.data)
        
        user = User.query.filter_by(email=request.form.get("username")).first()
        
        if user and bcrypt.check_password_hash(
            user.password, request.form.get("password")
        ):
            login_user(user)
            return redirect(url_for("skills"))
            
    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        user = User(username=username, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route("/todo", methods=["GET", "POST"])
@login_required
def tasks():
    curr_user = current_user.id
    todo = Todo.query.filter_by(user_id=curr_user).all()
    
    task_info=[]
    """
    todo info title,adddate, duedate
    task info title,priority, label, datetime
    """

    return render_template("tasks.html", todo=todo, task_info=task_info)





@app.route("/todo/tasks", methods=["GET", "POST"])
@login_required
def query_task():
    var = request.args.get("my_var")
    # var may be priority -> [1, 2, 3], datetime, label -> [personal, work, shopping, other]
    task = Tasks.query.filter_by().all()
    return render_template("query_task.html", task=task, var=var)


@app.route("/todo/add_task", methods=["GET", "POST"])
@login_required
def add_task():
    var = request.args.get("my_var")
    if request.method == "POST":
        title = request.form.get("title")
        """
        title,
        adddate,
        duedate,
        priority -> [1, 2, 3],
        label -> [personal, work, shopping, other]
        status -> [new, progess, completed]
        """
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add_task.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")
