#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The core module holds generic functions and the Flask extensions.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_oauthlib.provider import OAuth2Provider


db = SQLAlchemy()
oauth = OAuth2Provider()
