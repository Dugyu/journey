from journeyapp import db
from datetime import datetime
from datetime import date
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    image_file = db.Column(db.String(70), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    stations = db.relationship('Station', backref='seer', lazy=True)
    events = db.relationship('Event', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    latitude = db.Column(db.Numeric(10,7), nullable=False, default=39.9931568)
    longtitude = db.Column(db.Numeric(10,7), nullable=False, default=116.3375482)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}')"

class Station(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    latitude = db.Column(db.Numeric(10,7), nullable=False, default=39.9931568)
    longtitude = db.Column(db.Numeric(10,7), nullable=False, default=116.3375482)
    timeinfo = db.Column(db.Text, nullable=False)
    feature = db.Column(db.Text,nullable=False)
    abstract = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(70), nullable=False, default="default.jpg")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    events = db.relationship('Event', backref='station', lazy=True)
    journals = db.relationship('Journal', backref='station', lazy=True)
    def __repr__(self):
        return f"Station('{self.name}','{self.latitude}','{self.longtitude}','{self.image_file}', '{self.timeinfo}','{self.feature}')"

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image_file = db.Column(db.String(70), nullable=False, default="default.jpg")
    date = db.Column(db.Date, nullable=False, default=date.today())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    station_id = db.Column(db.Integer, db.ForeignKey("station.id"), nullable=False)
    journals = db.relationship('Journal', backref='event', lazy=True)
    def __repr__(self):
        return f"Event('{self.name}','{self.date}','{self.station_id}')"

class Journal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"), nullable=False)
    station_id = db.Column(db.Integer, db.ForeignKey("station.id"), nullable=False)
    jourimages = db.relationship('Jourimage', backref='journal',lazy=True)
    def __repr__(self):
        return f"Journal('{self.title}','{self.date_posted}', '{self.station_id}')"

class Jourimage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(70), nullable=False, default="default.jpg")
    journal_id = db.Column(db.Integer, db.ForeignKey("journal.id"), nullable=False)
    def __repr__(self):
        return f"Jourimage('{self.filename}')"