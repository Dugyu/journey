import requests
import urllib.parse
import secrets
import os
from PIL import Image

from journeyapp import app
from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def save_image(imagedata,maxpixel,address):
    random_hex = secrets.token_hex(8)
    _, file_extension = os.path.splitext(imagedata.filename)
    image_fn = random_hex + file_extension
    image_path = os.path.join(app.root_path, 'static/'+address+'/', image_fn)

    image = Image.open(imagedata)
    
    img_width = image.size[0]
    img_height = image.size[1]
    
    
    if img_width > img_height:
        img_width = round(img_width/img_height) * maxpixel
        img_height = maxpixel
    else:
        img_height = round(img_height/img_width) * maxpixel
        img_width = maxpixel
    
    resized_image = image.resize((img_width,img_height))
    box = (0.5*(img_width - maxpixel) , 0.5*(img_height - maxpixel), 0.5*(img_width + maxpixel), 0.5*(img_height + maxpixel))
    cropped_image = resized_image.crop(box)
    cropped_image.save(image_path)

    return image_fn

def decideCity(lat,lng):
    if lat > 0 and lng > 0:
        return "beijing"
    elif lat < 0 and lng > 0:
        return "jakarta"
    else:
        return "boston"