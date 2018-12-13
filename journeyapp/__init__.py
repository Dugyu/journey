from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_s3 import FlaskS3
from tempfile import mkdtemp
import os

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
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['POSTGRE_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Database
db = SQLAlchemy(app)

# S3 bucket
app.config['FLASKS3_BUCKET_NAME'] = os.environ['S3_BUCKET_NAME']
app.config['AWS_ACCESS_KEY_ID'] = os.environ['AWS_ACCESS_KEY_ID']
app.config['AWS_SECRET_ACCESS_KEY'] = os.environ['AWS_SECRET_ACCESS_KEY']
app.config['FLASKS3_HEADERS'] =    {'Expires': 'Mon, 31 Dec 2018 20:00:00 GMT'}
app.config['S3_LOCATION'] = 'http://{}.s3.amazonaws.com/'.format(app.config['FLASKS3_BUCKET_NAME'])

s3 = FlaskS3(app)

def strlen(s):
    return len(s)
def string(s):
    return str(s)
app.jinja_env.globals.update(strlen=strlen)
app.jinja_env.globals.update(string=string)
from journeyapp import routes