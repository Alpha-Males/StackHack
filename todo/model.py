"""


"""

from todo import db, login_manager
from flask_login import UserMixin
import datetime
from flask_login import current_user


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120),nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    tasks = db.relationship("Tasks", backref="user", lazy=True, passive_deletes=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"





class Tasks(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    adddate = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    duedate = db.Column(db.DateTime)
    label = db.Column(db.String(100), nullable=False)
    priority = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(100), nullable=False)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )

    def __repr__(self):
        return f"Todo('{self.id}' '{self.title}','{self.adddate}','{self.duedate}','{self.user_id}','{self.label}','{self.priority}','{self.status}')"
