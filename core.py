from flask_sqlalchemy import SQLAlchemy
from flask_oauthlib.provider import OAuth2Provider
#from validator import MyRequestValidator

# The core module is used to hold generic functions and the flask extensions

db = SQLAlchemy()

oauth = OAuth2Provider()
