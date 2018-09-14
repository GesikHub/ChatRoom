from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
login = LoginManager()
login.login_view = 'login.login'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    login.init_app(app)

    from application.main import bp as bp_main
    app.register_blueprint(bp_main)
    from application.auth import bp as bp_login
    app.register_blueprint(bp_login)
    from application.chat import bp as bp_chat
    app.register_blueprint(bp_chat)

    from application import models

    return app
