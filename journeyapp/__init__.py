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
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://strxotrpnncsmg:80a6ecbd2831b8437f3a026915b8f23c7a5f820be02c812a3726c7d66ff12398@ec2-54-227-249-201.compute-1.amazonaws.com:5432/d6ojd8vt630glk'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Database
db = SQLAlchemy(app)

def strlen(s):
    return len(s)
app.jinja_env.globals.update(strlen=strlen)

from journeyapp import routes