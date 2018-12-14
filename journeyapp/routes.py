import re
import logging
from flask import flash, jsonify, redirect, render_template, request, session, url_for

from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import default_exceptions

from journeyapp import app,db
from journeyapp.helpers import apology, login_required, save_image, decideCity
from journeyapp.models import User, Post, Journal, Station, Jourimage, Event

import datetime


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/checkuser", methods=["GET"])
def checkuser():
    username = request.args.get("username")
    user = User.query.filter_by(username=username).first()
    """Return true if username available, else false, in JSON format"""
    if not user:
        return jsonify(True)
    else:
        return jsonify(False)


@app.route("/checkemail", methods=["GET"])
def checkemail():
    email = request.args.get("email")
    user = User.query.filter_by(email=email).first()
    """Return true if email available, else false, in JSON format"""
    if not user:
        return jsonify(True)
    else:
        return jsonify(False)


@app.route("/checklogin", methods=["GET"])
def checklogin():
    username = request.args.get("username")
    password = request.args.get("password")
    """Return true if user exists and password correct, else false, in JSON format"""
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        return jsonify(True)
    else:
        return jsonify(False)


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """Show user profile"""
    if request.method == "GET":
        page = request.args.get("page", 1, type=int)
        user = User.query.filter_by(id=session["user_id"]).first()
        image_file = url_for('static', filename='profile_pics/' + user.image_file)
        posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(per_page=4,page=page)
        return render_template("profile.html", user=user, posts=posts)
    else:
        user = User.query.filter_by(id=session["user_id"]).first()
        username = request.form.get("username")
        email = request.form.get("email")

        if username:
            username_exist = User.query.filter_by(username=username).first()
            if not username_exist:
                user.username = username
                db.session.commit()
            else:
                if username_exist.id != session["user_id"]:
                    return apology("Username already exists", 400)
        if email:
            email_exist = User.query.filter_by(email=email).first()
            if not email_exist:
                user.email = email
                db.session.commit()
            else:
                if email_exit.id != session["user_id"]:
                    return apology("Email already exists", 400)
        
        try:
            avatar = request.files["avatar"]
        except Exception:
            flash("Your profile has been updated!", 'success')
            return redirect("/profile")

        image_file = save_image(avatar,512,'profile_pics')
        user.image_file = image_file
        db.session.commit()
        
        flash("Your profile has been updated!", 'success')
        return redirect("/profile")


@app.route("/map/<string:city>", methods=["GET"])
def map(city):
    stations = Station.query.all()
    posts = Post.query.all()
    events = Event.query.all()
    station_data = []
    post_data = []
    event_data = []
    for station in stations:
        latitude = str(station.latitude)
        longtitude = str(station.longtitude)
        item = {
            'lat':latitude,
            'lng': longtitude,
            'name': station.name,
            'image': station.image_file,
            'timeinfo': station.timeinfo,
            'feature': station.feature,
            'abstract': station.abstract,
            'seer': station.seer.id,
            'id': station.id,
        }
        station_data.append(item)
    for post in posts:
        latitude = str(post.latitude)
        longtitude = str(post.longtitude)
        item = {
            'id':post.id,
            'lat':latitude,
            'lng': longtitude,
            'title': post.title,
            'content': post.content,
            'author': post.author.username
        }
        post_data.append(item)
    for event in events:
        latitude = str(event.station.latitude)
        longtitude = str(event.station.longtitude)
        item = {
            'id': event.id,
            'name': event.name,
            'image': event.image_file,
            'date': event.date.strftime('%Y-%m-%d'),
            'creator': event.user_id,
            'station': event.station_id,
            'journal': event.journals[0].content,
            'journal_id': event.journals[0].id,
            'lat': latitude ,
            'lng': longtitude
        }
        event_data.append(item)
    userinfo = {'isLoggedIn':False}
    try:
        user_id = session["user_id"]
        userinfo['isLoggedIn'] = True
        userinfo['session'] = user_id 
    except Exception:
        pass
    city_template = city + ".html"
    return render_template(city_template, stations = station_data, posts=post_data,events=event_data, userinfo=userinfo)


@app.route("/anchor/<string:anchor_id>/update", methods=["GET","POST"])
@login_required
def update_anchor(anchor_id):
    anchor_id = int(anchor_id)
    if request.method == "GET":
        station = Station.query.get(anchor_id)
        if not station:
            return apology("Station Not Found!", 403)
        url = str(anchor_id)+"/update"
        if station.seer.id != session["user_id"] and session["user_id"] > 3:
            return apology("You do not have access!", 403)
        return render_template("create_station.html", title="Update Station",\
        station=station, button_name="Update", url=url)
    else:
        # Ensure title was submitted
        if not request.form.get("title"):
            return apology("must provide title", 400)
        # Ensure location was submitted
        elif not request.form.get("latitude"):
            return apology("must provide latitude", 400)
        elif not request.form.get("longtitude"):
            return apology("must provide longtitude", 400)
        # Ensure info was submitted
        elif not request.form.get("timeinfo"):
            return apology("must provide timeinfo", 400)
        elif not request.form.get("feature"):
            return apology("must provide feature", 400)
        elif not request.form.get("abstract"):
            return apology("must provide abstract", 400)
        
        # Check uniqueness
        name = request.form.get("title")

        # Process data before add into database
        station = Station.query.get(anchor_id)
        name_exists = Station.query.filter_by(name=name).first()
        if not name_exists:
            station.name = name

        station.latitude = float(request.form.get("latitude"))
        station.longtitude = float(request.form.get("longtitude"))
        station.timeinfo = request.form.get("timeinfo")
        station.feature = request.form.get("feature")
        station.abstract = request.form.get("abstract")

        db.session.commit()
    
        cityname = decideCity(station.latitude,station.longtitude)
        try:
            avatar = request.files["avatar"]
        except Exception:

            flash("Station has been updated!", 'success')
            return redirect('/map/'+cityname)

        image_file = save_image(avatar,512,'station_pics')
        station.image_file = image_file
        db.session.commit()
        flash("Station has been updated!", 'success')
        return redirect("/map/" + cityname)


@app.route("/anchor/<string:anchor_id>/delete", methods=["POST"])
@login_required
def delete_station(anchor_id):
    anchor_id = int(anchor_id)
    station = Station.query.get(anchor_id)        
    if station.seer.id != session["user_id"] and session["user_id"] > 3:
        return apology("You do not have access!", 403)
    
    
    journals = Journal.query.filter_by(station=station)

    for journal in journals:    
        # Delete image childs first
        jourimages = Jourimage.query.filter_by(journal=journal).all()
        for jourimage in jourimages:
            db.session.delete(jourimage)
            db.session.commit()
        # Query Event
        event = journal.event
        # Delete journal
        db.session.delete(journal)
        db.session.commit()
        # Delete Event
        db.session.delete(event)
        db.session.commit()

    db.session.delete(station)
    db.session.commit()
    cityname = decideCity(station.latitude,station.longtitude)

    flash("Your station has been deleted!", 'success')
    return redirect("/map/" + cityname)


@app.route("/getmarkers", methods=["GET"])
def get_markers():
    stations = Station.query.all()
    data = []
    for station in stations:
        latitude = str(station.latitude)
        longtitude = str(station.longtitude)
        item = {
            'lat':latitude,
            'lng': longtitude,
            'title': station.name
        }
        data.append(item)
    return jsonify(data)


@app.route("/journal", methods=["GET"])
def journal():
    page = request.args.get("page", 1, type=int)
    journals = Journal.query.order_by(Journal.date_posted.desc()).paginate(per_page=3,page=page)
    return render_template("journal.html", journals = journals)


@app.route("/forum")
def forum():
    # Query Database with pagination
    page = request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=3,page=page)
    return render_template("forum.html", posts=posts)


@app.route("/station/<string:station_name>")
def station_public(station_name):
    # Query Database with pagination
    page = request.args.get("page", 1, type=int)
    station = Station.query.filter_by(name=station_name).first()
    if not station:
        return apology("This station does not exist!", 400)
    journals = Journal.query.filter_by(station=station)\
        .order_by(Journal.date_posted.desc())\
        .paginate(per_page=2,page=page)
    return render_template("station_public.html", journals=journals, station=station)


@app.route("/user/<string:username>")
def user_public(username):
    # Query Database with pagination
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first()
    if not user:
        return apology("This user does not exist!", 400)
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(per_page=3,page=page)
    return render_template("user_public.html", posts=posts, user=user)


@app.route("/report/new",methods=["GET","POST"])
@login_required
def new_report():
    if request.method == "GET":
        post = {"title": '', "content": ''} 
        return render_template("create_report.html", title="New Report",\
         post=post, button_name="Create",url="new")
    else:
        # Ensure title was submitted
        if not request.form.get("title"):
            return apology("must provide title", 400)
        # Ensure comment was submitted
        elif not request.form.get("comment"):
            return apology("must provide comment", 400)
        title = request.form.get("title")
        content = request.form.get("comment")
        user_current = User.query.filter_by(id=session["user_id"]).first()
        post = Post(title=title,content=content,author=user_current) 
        db.session.add(post)
        db.session.commit()

        if request.form.get("latitude"):
            post.latitude = request.form.get("latitude")
        if request.form.get("longtitude"):
            post.longtitude = request.form.get("longtitude")
        db.session.commit()
        flash("Your post has been created!", 'success')
        return redirect("/forum")


@app.route("/write/new",methods=["GET","POST"])
@login_required
def new_journal():
    if request.method == "GET":
        form = {"title": '', "content": ''} 
        selected = "Choose Station..."
        stations = Station.query.all()
        journal = {'title': '', 'content': ''}
        event = {'date':'', 'name':''}
        return render_template("create_journal.html", title="New Journal",\
        journal = journal,selected=selected, event=event, button_name="Create",url="new", stations=stations)
    else:
        # Ensure journal title was submitted
        if not request.form.get("title"):
            return apology("must provide title", 400)
        # Ensure journal content was submitted
        elif not request.form.get("content"):
            return apology("must provide content", 400)
        # Ensure event name was submitted
        elif not request.form.get("name"):
            return apology("must provide event name", 400)
        # Ensure date was set
        elif not request.form.get("datepicker"):
            return apology("must set a date for event", 400)
        # Ensure Station was picked
        elif not request.form.get("stationSelect"):
            return apology("must pick a station to go on", 400)
        
        name = request.form.get("name")
        event_date = request.form.get("datepicker")
        title = request.form.get("title")
        content = request.form.get("content")
        station_id = int(request.form.get("stationSelect"))
        
        # transfer date format
        event_date = datetime.date(int(event_date[0:4]), int(event_date[5:7]),int(event_date[8:10]))
        
        # check uniqueness
        event_exist = Event.query.filter_by(station_id=station_id).filter_by(name=name).filter_by(date=event_date).first()

        if event_exist:
            return apology("Event already exist!", 400)
        
        new_event = Event(name=name, date=event_date, user_id=session["user_id"], station_id=station_id)
        db.session.add(new_event)
        db.session.commit()
        event = Event.query.filter_by(station_id=new_event.station_id).filter_by(date=new_event.date).filter_by(name=new_event.name).first()
        new_journal = Journal(title=title,content=content,event=event,station=event.station)
        db.session.add(new_journal)
        db.session.commit()
        
        try:
            jourimages = request.files.getlist('jourimage')
        except Exception:
            jourimages = False
        if not jourimages:
            flash("Your journal has been created!", 'success')
            return redirect('/journal')
        
        image_file = save_image(jourimages[0],1024,'event_pics')
        event.image_file = image_file
        db.session.commit()
        journal = Journal.query.filter_by(event=event).first()

        for jourimage in jourimages:
            jourimage_file = save_image(jourimage,1024,'journal_pics')
            new_jourimage = Jourimage(filename=jourimage_file,journal=journal)
            db.session.add(new_jourimage)
            db.session.commit()
        flash("Your journal has been created!", 'success')
        return redirect("/journal")


@app.route("/anchor/new",methods=["GET","POST"])
@login_required
def new_anchor():
    # GET
    if request.method == "GET":
        station = {"title": '', "latitude": '', "longtitude": '', "timeinfo":'', "abstract": '', "feature":''} 
        return render_template("create_station.html", title="New Station",\
         station=station, button_name="Add",url="new")
    # POST
    else:
        # Ensure title was submitted
        if not request.form.get("title"):
            return apology("must provide title", 400)
        # Ensure location was submitted
        elif not request.form.get("latitude"):
            return apology("must provide latitude", 400)
        elif not request.form.get("longtitude"):
            return apology("must provide longtitude", 400)
        # Ensure info was submitted
        elif not request.form.get("timeinfo"):
            return apology("must provide timeinfo", 400)
        elif not request.form.get("feature"):
            return apology("must provide feature", 400)
        elif not request.form.get("abstract"):
            return apology("must provide abstract", 400)
        
        # Check uniqueness
        name = request.form.get("title")
  
        # Process data before add into database
        station = Station.query.filter_by(name=name).first()
        if station:
             return apology("this station name already exists!", 400)

        latitude = float(request.form.get("latitude"))
        longtitude = float(request.form.get("longtitude"))
        timeinfo = request.form.get("timeinfo")
        feature = request.form.get("feature")
        abstract = request.form.get("abstract")
        
        user_current = User.query.filter_by(id=session["user_id"]).first()
        station = Station(name=name,latitude=latitude,longtitude=longtitude,timeinfo=timeinfo,feature=feature,abstract=abstract,seer=user_current)        
        db.session.add(station)
        db.session.commit()
    
        cityname = decideCity(station.latitude,station.longtitude)

        try:
            avatar = request.files["avatar"]
        except Exception:
            flash("Station has been added to our map!", 'success')
            return redirect('/map/' + cityname)
        
        image_file = save_image(avatar,512,'station_pics')
        station.image_file = image_file
        db.session.commit()

        flash("Station has been added to our map!", 'success')
        return redirect("/map/"+cityname)

@app.route("/journal/<int:journal_id>")
def single_journal(journal_id):
    journal = Journal.query.get(journal_id)
    if not journal:
        return apology("Journal Not Found!", 403)
    jourimages = Jourimage.query.filter_by(journal=journal).all()
    return render_template('single_journal.html', title=journal.title, journal=journal, jourimages=jourimages)

@app.route("/report/<int:report_id>")
def report(report_id):
    post = Post.query.get(report_id)
    if not post:
        return apology("Report Not Found!", 403)
    return render_template('comment.html', title=post.title, post=post)


@app.route("/write/<int:journal_id>/update", methods=["GET","POST"])
@login_required
def update_journal(journal_id):
    if request.method == "GET":
        journal = Journal.query.get(journal_id)
        selected = journal.station.name
        stations = []
        event = journal.event
        if not journal:
            return apology("Journal Not Found!", 403)
        if journal.event.user_id != session["user_id"] and session["user_id"] > 3:
            return apology("You do not have access!", 403)
        url = str(journal_id)+"/update"
        return render_template("create_journal.html", title="Update Journal",\
        journal=journal, event=event, selected=selected,stations=stations, button_name="Update", url=url)

    else:
        journal = Journal.query.get(journal_id)
        event = journal.event

        # Ensure journal title was submitted
        if not request.form.get("title"):
            return apology("must provide title", 400)
        # Ensure journal content was submitted
        elif not request.form.get("content"):
            return apology("must provide content", 400)
        # Ensure event name was submitted
        elif not request.form.get("name"):
            return apology("must provide event name", 400)
        # Ensure date was set
        elif not request.form.get("datepicker"):
            return apology("must set a date for event", 400)
        # Station was set as a default, no need to check
        
        name = request.form.get("name")
        event_date = request.form.get("datepicker")
        title = request.form.get("title")
        content = request.form.get("content")
        
        # transfer date format
        event_date = datetime.date(int(event_date[0:4]), int(event_date[5:7]),int(event_date[8:10]))
        
        # check uniqueness
        event_exist = Event.query.filter_by(station_id=journal.station.id).filter_by(name=name).filter_by(date=event_date).first()

        if event_exist and (event_exist.id != event.id):
            return apology("Event already exist!", 400)
        
        event.name = name
        event.date = event_date
        journal.title = title
        journal.content = content
        db.session.commit()
        
        try:
            jourimages = request.files.getlist('jourimage')
        except Exception:
            jourimages = False

        if not jourimages:
            flash("Your journal has been updated!", 'success')
            return redirect('/journal')
        
        image_file = save_image(jourimages[0],1024,'event_pics')
        event.image_file = image_file
        db.session.commit()

        old_jourimages = Jourimage.query.filter_by(journal=journal).all()
        for oldimage in old_jourimages:
            db.session.delete(oldimage)
            db.session.commit()
        for jourimage in jourimages:
            jourimage_file = save_image(jourimage,1024,'journal_pics')
            new_jourimage = Jourimage(filename=jourimage_file,journal=journal)
            db.session.add(new_jourimage)
            db.session.commit()
        flash("Your journal has been updated!", 'success')
        return redirect("/journal")

@app.route("/report/<int:report_id>/update", methods=["GET","POST"])
@login_required
def update_report(report_id):
    if request.method == "GET":
        post = Post.query.get(report_id)
        if not post:
            return apology("Report Not Found!", 403)
        if post.author.id != session["user_id"] and session["user_id"] > 3:
            return apology("You do not have access!", 403)
        url = str(report_id)+"/update"
        return render_template("create_report.html", title="Update Report",\
        post=post, button_name="Update", url=url)
    else:
        # Ensure title was submitted
        if not request.form.get("title"):
            return apology("must provide title", 400)
        # Ensure password was submitted
        elif not request.form.get("comment"):
            return apology("must provide comment", 400)
        post = Post.query.get(report_id)
        post.title = request.form.get("title")
        post.content = request.form.get("comment")
        db.session.commit()
        flash("Your comment has been updated!", 'success')
        return redirect("/forum")


@app.route("/write/<int:journal_id>/delete", methods=["POST"])
@login_required
def delete_journal(journal_id):
        journal = Journal.query.get(journal_id)
        if journal.event.user_id != session["user_id"] and session["user_id"] > 3:
            return apology("You do not have access!", 403)
        
        # Delete image childs first
        jourimages = Jourimage.query.filter_by(journal=journal).all()
        for jourimage in jourimages:
            db.session.delete(jourimage)
            db.session.commit()
        # Query Event
        event = journal.event
        # Delete journal
        db.session.delete(journal)
        db.session.commit()
        # Delete Event
        db.session.delete(event)
        db.session.commit()
        flash("Your journal has been deleted!", 'success')
        return redirect("/journal")


@app.route("/report/<int:report_id>/delete", methods=["POST"])
@login_required
def delete_report(report_id):
        post = Post.query.get(report_id)
        if post.author.id != session["user_id"] and session["user_id"] > 3:
            return apology("You do not have access!", 403)
        db.session.delete(post)
        db.session.commit()
        flash("Your post has been deleted!", 'success')
        return redirect("/forum")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must confirm password", 400)

        # Query database for username and email
        username = User.query.filter_by(username=request.form.get("username")).first()
        email = User.query.filter_by(email=request.form.get("email")).first()
        
        # Ensure username is and password is same
        if username:
            return apology("username is taken", 400)
        
        elif email:
            return apology("email is taken", 400)

        # Ensure passwords and confirmation match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords do not match", 400)
        
        user_current=User(username=request.form.get("username"),email=request.form.get("email"),password=generate_password_hash(request.form.get("password")))
        db.session.add(user_current)
        db.session.commit()
        flash(f"Account created for {user_current.username} !", "success")

        # Remember which user has logged in
        session["user_id"] = user_current.id

        # Redirect user to home page
        return redirect("/profile")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        user = User.query.filter_by(username=request.form.get("username")).first()

        # Ensure username exists and password is correct
        if not user or not check_password_hash(user.password, request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = user.id

        flash(f"Welcome back {user.username} !", "success")

        # Redirect user to profile page
        return redirect("/profile")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")



@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to home page form
    return redirect("/")

def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)

# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)