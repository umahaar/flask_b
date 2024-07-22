import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'supersecretkey'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:example@mariadb/flask_db'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:example@db/flaskdb'