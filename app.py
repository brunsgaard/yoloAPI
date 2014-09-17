from flask import Flask
from flask import render_template
from models import db, User, Client
from flask import request
from flask_oauthlib.provider import OAuth2Provider
from validator import MyRequestValidator
import logging

# Show us some logging info from flask_aouthlib
logger = logging.getLogger('flask_oauthlib')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


# Flask app
app = Flask(__name__)
app.debug = True
app.config.update(
    {
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///db.sqlite',
        'DEBUG': True
    }
)

# Setup database
db.init_app(app)

# Prepare flask_oauthlib Provider
oauth = OAuth2Provider(app)
oauth._validator = MyRequestValidator()


# set endpoint for token handler
@app.route('/oauth/token', methods=['POST'])
@oauth.token_handler
def access_token(*args, **kwargs):
    # Returns a dictionary or None as the extra credentials
    # for creating the token response.
    return None


# This is our little mangement interface for creating test users and clients
@app.route('/', methods=['GET', 'POST'])
def management():
    if request.method == 'POST' and request.form['submit'] == 'adduser':
        User.save(request.form['username'], request.form['password'])
    if request.method == 'POST' and request.form['submit'] == 'addclient':
        Client.generate()
    return render_template('management.html', users=User.all(),
                           clients=Client.all())


# The resource we are trying to protect
@app.route('/yolo')
@oauth.require_oauth()
def yolo():
    return "YOLO!!!, you made it through"


if __name__ == '__main__':
    db.create_all(app=app)
    app.run()
