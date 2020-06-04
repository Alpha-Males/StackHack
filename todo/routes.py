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


from datetime import datetime
import os
import requests
import secrets
# import urllib


from flask import render_template, flash, url_for, redirect, request
from flask_login import login_user, current_user, login_required, logout_user
from PIL import Image


from todo import app, db, bcrypt
from todo.model import User, Tasks



allowed_extensions = ["jpg", "png", "ppm"]





def checkavl(email,username):
    user=User.query.filter_by(username=username).first()
    if user:
        return False
    user=User.query.filter_by(email=email).first()
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
    if request.method == "POST":

        user = User.query.filter_by(email=request.form.get("username")).first()
        print(user.password)
        if user and bcrypt.check_password_hash(
            user.password, request.form.get("password")
        ):
            login_user(user)
            return redirect(url_for("tasks"))
        else:
            flash(u'Invalid password provided', 'error')
            return redirect('/login')

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    fields = {}
    fields['route'] = 'register'

    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm = request.form.get("confirm")

        if password == confirm and checkavl(email,username):
            hashed_password = bcrypt.generate_password_hash(password)
            fields['username'] = username
            fields['email'] = email
            fields['password'] = hashed_password
            # API to interact with backend to POST data
            res=requests.post('http://127.0.0.1:5000/todores/id',data=fields)
            if res:
                pass
                # ...
            return redirect(url_for("login"))

        else:
            flash(u'validation error', 'error')

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

    ids=request.args.to_dict()
    if ids:
        ids = ids['id'].split(':')
        task = Tasks.query.filter(Tasks.id.in_(ids)).all()

        return render_template("task.html",tasks=task)

    return render_template("task.html",tasks=task)


@app.route("/query_tasks", methods=["GET", "POST"])
@login_required
def query_task():

    priority = ['argent', 'important', 'do-it-now']
    label = ['personal', 'work', 'shopping', 'other']
    status = ['new', 'progess', 'completed']

    if request.method == "POST":
        due_date = request.form.get("duedate")
        priority = request.form.get("priority")
        status = request.form.get("status")
        label = request.form.get("label")

        task = Tasks.query.filter_by(priority=priority,duedate=due_date,user_id=curr_user).all()
        id=''
        for i in task:
            id+=':'+str(i.id)
        return redirect(url_for("tasks",id=id))

    return render_template("query_task.html",priority=priority, label=label, status=status)


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
    priority = ['argent', 'important', 'do-it-now']
    label = ['personal', 'work', 'shopping', 'other']
    status = ['new', 'progess', 'completed']
    if request.method == "POST":
        title = request.form.get("title")
        add_date = datetime.now()
        due_date = request.form.get("duedate")
        priority = request.form.get("priority")
        status = request.form.get("status")
        label = request.form.get("label")

        fields = {}
        fields['route'] = 'add_task'
        fields['title'] = title
        fields['add_date'] = add_date
        fields['due_date'] = due_date
        fields['priority'] = priority
        fields['status'] = status
        fields['label'] = label
        fields['curr_user'] =curr_user

        # API to interact with backend to POST data
        res=requests.post('http://127.0.0.1:5000/todores/id',data=fields)
        if res:
            pass
            # ...
        return redirect(url_for("home"))
    return render_template("add_task.html", priority=priority, label=label, status=status)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")
