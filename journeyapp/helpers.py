import requests
import urllib.parse
import secrets
import os
import io
from PIL import Image
import boto3, botocore

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


s3 = boto3.client(
   "s3",
   aws_access_key_id=app.config["AWS_ACCESS_KEY_ID"],
   aws_secret_access_key=app.config["AWS_SECRET_ACCESS_KEY"]
)

def upload_file_to_s3(file_object, image_path, image_ext, bucket_name, acl="public-read"):

    try:
        s3.upload_fileobj(
            file_object,
            bucket_name,
            image_path,
            ExtraArgs={
                "ACL": acl,
                "ContentType": image_ext
            }
        )

    except Exception as e:
        print("File Upload Faild: ", e)
        return e

    return "{}{}".format(app.config["S3_LOCATION"],image_path)

#for s3 bucket
def save_image(imagedata,maxpixel,address):
    random_hex = secrets.token_hex(8)
    _, file_extension = os.path.splitext(imagedata.filename)
    image_fn = random_hex + file_extension
    image_path = os.path.join('static/'+address+'/', image_fn)

    image = Image.open(imagedata)
    img_width = image.size[0]
    img_height = image.size[1]

    if img_width > img_height:
        img_width = round(img_width/img_height * maxpixel)
        img_height = maxpixel
    else:
        img_height = round(img_height/img_width * maxpixel)
        img_width = maxpixel

    resized_image = image.resize((img_width,img_height))
    box = (0.5*(img_width - maxpixel) , 0.5*(img_height - maxpixel), 0.5*(img_width + maxpixel), 0.5*(img_height + maxpixel))
    cropped_image = resized_image.crop(box)
    
    #saving image to cStringIO object
    out_img = io.BytesIO()

    cropped_image.save(out_img, format=image.format)
    # the cursor is at the end after reading, rewind it back
    out_img.seek(0)
    
    upload_file_to_s3(out_img,image_path, image.format, app.config['FLASKS3_BUCKET_NAME'])

    return image_fn

#for local

'''
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
'''

def decideCity(lat,lng):
    if lat > 0 and lng > 0:
        return "beijing"
    elif lat < 0 and lng > 0:
        return "jakarta"
    else:
        return "boston"