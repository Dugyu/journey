from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

from tempfile import mkdtemp


# App
app = Flask(__name__)


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://omfgiyhxovsdia:85689f7ebbec3b5a3b901287465ae865c2aff766454a9ca9027e55323992d757@ec2-54-243-150-10.compute-1.amazonaws.com:5432/d91d5sfeo9tll2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Database
db = SQLAlchemy(app)

def strlen(s):
    return len(s)
app.jinja_env.globals.update(strlen=strlen)

from journeyapp import routes