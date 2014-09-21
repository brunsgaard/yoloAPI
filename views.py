from flask import Blueprint, render_template, request
from models import Client, User
from core import oauth

yoloapi = Blueprint('yoloApi', __name__)

# set endpoint for token handler
@yoloapi.route('/oauth/token', methods=['POST'])
@oauth.token_handler
def access_token(*args, **kwargs):
    # Returns a dictionary or None as the extra credentials
    # for creating the token response.
    return None


# This is our little mangement interface for creating test users and clients
@yoloapi.route('/', methods=['GET', 'POST'])
def management():
    if request.method == 'POST' and request.form['submit'] == 'adduser':
        User.save(request.form['username'], request.form['password'])
    if request.method == 'POST' and request.form['submit'] == 'addclient':
        Client.generate()
    return render_template('management.html', users=User.all(),
                           clients=Client.all())


# The resource we are trying to protect
@yoloapi.route('/yolo')
@oauth.require_oauth()
def yolo():
    return "YOLO!!! You made it through and accessed the protected resource"
