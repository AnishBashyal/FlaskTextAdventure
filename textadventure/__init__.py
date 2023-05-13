import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

login_manager.login_view  = 'user.login'
login_manager.login_message_category = 'info'

from textadventure.main.routes import main
from textadventure.user.routes import user
from textadventure.story.routes import story

app.register_blueprint(main)
app.register_blueprint(user)
app.register_blueprint(story)



