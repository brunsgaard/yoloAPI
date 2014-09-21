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




if __name__ == '__main__':
    db.create_all(app=app)
    app.run()
