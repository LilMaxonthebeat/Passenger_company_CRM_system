import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = Fernet.generate_key()
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENCRYPTION_KEY = Fernet.generate_key()
