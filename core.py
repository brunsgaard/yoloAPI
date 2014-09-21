"""
The core module holds generic functions and the flask extensions
"""

from flask_sqlalchemy import SQLAlchemy
from flask_oauthlib.provider import OAuth2Provider


db = SQLAlchemy()
oauth = OAuth2Provider()
