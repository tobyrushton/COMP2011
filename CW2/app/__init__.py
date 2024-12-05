from flask import Flask, request, session
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_babel import Babel
from flask_wtf.csrf import CSRFProtect
from .filters import time_ago

# create flask app
app = Flask(__name__)
# load config from config.py
app.config.from_object('config')
# add filter to create the time ago function
app.jinja_env.filters['time_ago'] = time_ago
# init db
db = SQLAlchemy(app)
# init csrf to allow for ajax
csrf = CSRFProtect(app)
# init migrate
migrate = Migrate(app, db)
# init login manager
login_manager = LoginManager()
login_manager.init_app(app)

# set up admin page
babel = Babel(app)
admin = Admin(app)
from flask_admin.contrib.sqla import ModelView
from app.models import User, Post, Like
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Like, db.session))
admin.add_view(ModelView(models.Comment, db.session))

from app import views, models