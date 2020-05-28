"""
Get request working 

"""

from flask import request 
from flask_restful import Resource,reqparse

from todo.model import User,Tasks
from todo import db

parser = reqparse.RequestParser()
parser.add_argument('task')

class TodoRes(Resource):
	def get(self,ids):
		tasks = {}
		if ids:
			ids=ids.split(':')
			task = Tasks.query.filter(Tasks.id.in_(ids)).all()
			tasks['id'] = task[0].title
		return tasks

	def post(self):
		args = request.form['task']
		# working for curl
		# curl http://127.0.0.1:5000/todores/id -d "task=something new"
		return args








