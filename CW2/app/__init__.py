from flask import Flask, request, session
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_babel import Babel
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
csrf = CSRFProtect(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)

babel = Babel(app)
admin = Admin(app)
from flask_admin.contrib.sqla import ModelView
from app.models import User
admin.add_view(ModelView(User, db.session))

from app import views, models