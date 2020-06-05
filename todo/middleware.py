"""
Get request working

"""
from datetime import datetime
import json

from flask import request
from flask_restful import Resource, reqparse

from todo.model import User, Tasks
from todo import db


class TodoRes(Resource):
    def get(self, ids):
        tasks = {}
        if ids:
            ids = ids.split(":")
            task = Tasks.query.filter(Tasks.id.in_(ids)).all()
            # print(task[0].__dict__)
        return tasks

    def post(self):
        if request.form["route"] == "add_task":
            title = request.form["title"]
            add_date = datetime.now()
            due_date = request.form["due_date"]
            due_date = datetime.strptime(due_date, "%Y-%m-%d")
            priority = request.form["priority"]
            status = request.form["status"]
            label = request.form["label"]
            curr_user = request.form["curr_user"]
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
            # working for curl
        # curl http://127.0.0.1:5000/todores/id -d "task=something new"
        if request.form["route"] == "register":
            username = request.form["username"]
            email = request.form["email"]
            password = request.form["password"]
            user = User(username=username, email=email, password=password)
            db.session.add(user)
            db.session.commit()
        return "ok"
