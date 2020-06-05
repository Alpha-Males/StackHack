"""
Routes:

home -->
about -->
account -->
login -->
register -->
tasks -->
query_task -->
add_task -->
logout -->


"""

# User Auth with REST architecture is provided only after doing some research.
# Apart from User Auth everything must interact with ORM throug a middleware having REST architecture


# key = crpt.key_derive(b"data")  # api to calculate key using PKCS7
# crpt.key_verify(b"data", key)  # api to verify the key

from datetime import datetime
import os
import requests
import secrets
import hashlib

# import urllib


from flask import render_template, flash, url_for, redirect, request
from flask_login import login_user, current_user, login_required, logout_user
from flask_dance.contrib.github import make_github_blueprint, github
from PIL import Image


from todo import app, db, bcrypt
from todo.model import User, Tasks


allowed_extensions = ["jpg", "png", "ppm"]

app.config["GITHUB_OAUTH_CLIENT_ID"] = "0cd2c183c8cefac1daf6"
app.config["GITHUB_OAUTH_CLIENT_SECRET"] = "bd615912c583831900cda5bb8c27856664e18d6c"
github_bp = make_github_blueprint()
app.register_blueprint(github_bp, url_prefix="/login")


def checkavl(email, username):
    user = User.query.filter_by(username=username).first()
    if user:
        return False
    return True


@app.route("/")
def home():
    """
    page for login and signup
    """
    return render_template("home.html")


@app.route("/about")
def about():
    """

    """
    return render_template("about.html")


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
    pro_pic = url_for("static", filename="profile_pics/" + current_user.image_file)
    if request.method == "POST":
        file = request.files.get("file")
        picture_file = save_and_upload(file)
        current_user.image_file = picture_file
        db.session.commit()
        return redirect(url_for("account"))
    return render_template("account.html", pro_pic=pro_pic)


@app.route("/loging")
def loging():
    if not github.authorized:
        return redirect(url_for("github.login"))
    resp = github.get("/user")
    username = resp.json()["login"]
    email = resp.json()["email"]
    print(username, email)
    user = User.query.filter_by(username=username).first()
    if user == None and checkavl(email, username) == True:
        user = User(username=username, email=email, password="no need")
        db.session.add(user)
        db.session.commit()
    # else:
    # login_user(user)
    login_user(user)
    return redirect(url_for("tasks"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    var = request.args.get("my_var")
    if var == "regg":
        return redirect(url_for("loging"))
    elif request.method == "POST":
        user = User.query.filter_by(email=request.form.get("username")).first()
        if (
            user
            and user.password
            == hashlib.sha224(request.form.get("password").encode("utf-8")).hexdigest()
        ):
            login_user(user)
            return redirect(url_for("tasks"))
        else:
            flash(u"Invalid password provided", "error")
            return redirect("/login")
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    fields = {}
    fields["route"] = "register"

    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm = request.form.get("confirm")

        if password == confirm and checkavl(email, username):
            hashed_password = hashlib.sha224(password.encode("utf-8")).hexdigest()
            user = User(username=username, email=email, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("login"))

        else:
            flash(u"validation error", "error")

    return render_template("register.html")


@app.route("/tasks", methods=["GET", "POST"])
@login_required
def tasks():
    """
    task info title,adddate,duedate,priority, label, datetime

    """
    curr_user = current_user.id

    # get request with a string having list of ids

    task = []

    task = Tasks.query.filter_by(user_id=curr_user).all()

    ids = request.args.to_dict()
    if ids:
        ids = ids["id"].split(":")
        task = Tasks.query.filter(Tasks.id.in_(ids)).all()

        return render_template("task.html", tasks=task)

    return render_template("task.html", tasks=task)


@app.route("/query_tasks", methods=["GET", "POST"])
@login_required
def query_task():
    curr_user = current_user.id
    priority = ["argent", "important", "do-it-now"]
    label = ["personal", "work", "shopping", "other"]
    status = ["new", "progess", "completed"]

    if request.method == "POST":
        due_date = request.form.get("duedate")
        due_date = datetime.strptime(due_date, "%Y-%m-%d")
        priority = request.form.get("priority")
        status = request.form.get("status")
        label = request.form.get("label")
        
        task = Tasks.query.filter_by(
            priority=priority, duedate=due_date, user_id=curr_user
        ).all()
        
        id = ""
        for i in task:
            id += ":" + str(i.id)
        return redirect(url_for("tasks", id=id))

    return render_template(
        "query_task.html", priority=priority, label=label, status=status
    )


@app.route("/add_task", methods=["GET", "POST"])
@login_required
def add_task():
    """
    title,
    adddate,
    duedate,
    priority -> ['argent', 'important', 'do-it-now'],
    label -> [personal, work, shopping, other],
    status -> [new, progess, completed]
    A REST api call to insert data into the database
    test object must be serialized

    """
    curr_user = current_user.id
    print(curr_user)
    priority = ["argent", "important", "do-it-now"]
    label = ["personal", "work", "shopping", "other"]
    status = ["new", "progess", "completed"]
    if request.method == "POST":
        title = request.form.get("title")
        add_date = datetime.now()
        due_date = request.form.get("duedate")
        due_date = datetime.strptime(due_date, "%Y-%m-%d")
        priority = request.form.get("priority")
        status = request.form.get("status")
        label = request.form.get("label")
        task = Tasks(
            title=title,
            adddate=add_date,
            duedate=due_date,
            priority=priority,
            status=status,
            label=label,
            user_id=curr_user,
        )
        db.session.add(task)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template(
        "add_task.html", priority=priority, label=label, status=status
    )


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")
