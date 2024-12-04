from flask import Flask, request, session
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_babel import Babel
from flask_wtf.csrf import CSRFProtect
from .filters import time_ago

app = Flask(__name__)
app.config.from_object('config')
app.jinja_env.filters['time_ago'] = time_ago
db = SQLAlchemy(app)
csrf = CSRFProtect(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)

babel = Babel(app)
admin = Admin(app)
from flask_admin.contrib.sqla import ModelView
from app.models import User, Post, Like
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Like, db.session))

from app import views, models