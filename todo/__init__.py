"""

"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
from flask_restful import Api

#
app = Flask(__name__)
app.config["SECRET_KEY"] = "5791628bb0b13ce0c676dfde280ba245"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

#
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
api = Api(app)


#
login_manager.login_view = "login"
login_manager.login_manager_category = "info"

#
UPLOAD_FOLDER = "todo/static/profile_pics"
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}

#
from todo import routes

from todo.middleware import TodoRes

api.add_resource(TodoRes, '/todores/<string:ids>','/todores/id')
