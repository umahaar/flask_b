from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from os import path

db = SQLAlchemy()
migrate = Migrate()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "supersecretkey"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    migrate.init_app(app, db)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User, Post

    print(f"Database path: {path.abspath(DB_NAME)}")  # Add this line
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    db_path = path.abspath(DB_NAME)
    print(f"Database path: {db_path}")  # Debug: Print the database path

    if not path.exists(db_path):
        with app.app_context():
            print("Creating database...")  # Debug: Indicate database creation
            db.create_all()
            print("Created database!")  # Debug: Indicate database was created
    else:
        print("Database already exists.")

