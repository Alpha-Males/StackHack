"""
Routes:
 
home -->
save_and_upload -->
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
import secrets
# import urllib


from flask import render_template, flash, url_for, redirect, request
from flask_login import login_user, current_user, login_required, logout_user
from PIL import Image


from todo import app, db, bcrypt
from todo.model import User, Tasks
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
    if request.method == "POST":
        print(form.email.data)
        
        user = User.query.filter_by(email=request.form.get("username")).first()
        print(user.password)
        if user and bcrypt.check_password_hash(
            user.password, request.form.get("password")
        ):
            login_user(user)
            return redirect(url_for("tasks"))
            
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
        hashed_password = bcrypt.generate_password_hash(password)
        user = User(username=username, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route("/tasks", methods=["GET", "POST"])
@login_required
def tasks():
    curr_user = current_user.id
    
    # get request with a string haing list of ids

    task=[]
    
    ids=request.args.to_dict()
    if ids:
        ids=ids['id'].split(':')
        task = Tasks.query.filter(Tasks.id.in_(ids)).all()
        return render_template("task.html",tasks=task)
            
    task = Tasks.query.filter().all()

    """
    task info title,adddate,duedate,priority, label, datetime
    """
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

        task = Tasks.query.filter_by(priority=priority).all()
        id=''
        for i in task:
            id+=':'+str(i.id)
        return redirect(url_for("tasks",id=id))

    return render_template("query_task.html",priority=priority, label=label, status=status)


@app.route("/add_task", methods=["GET", "POST"])
@login_required
def add_task():
    curr_user = current_user.id
    priority = ['argent', 'important', 'do-it-now']
    label = ['personal', 'work', 'shopping', 'other']
    status = ['new', 'progess', 'completed']
    if request.method == "POST":
        title = request.form.get("title")
        add_date = datetime.now()
        due_date = request.form.get("duedate")
        due_date = datetime.strptime(due_date, '%Y-%m-%d')
        priority = request.form.get("priority")
        status = request.form.get("status")
        label = request.form.get("label")

        # post request with json object having these fields

        task=Tasks(title=title,adddate=add_date,
            duedate=due_date,priority=priority,status=status,label=label,user_id=curr_user)
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
        db.session.add(task)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add_task.html", priority=priority, label=label, status=status)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")